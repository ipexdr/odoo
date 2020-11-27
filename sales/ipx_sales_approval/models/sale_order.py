# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging
import re

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = ['sale.order']

    # Overriding original state to add To Approve
    state = fields.Selection([
        ('draft', 'Quotation'),
        ('to approve', 'To Approve'),
        ('sent', 'Quotation Sent'),
        ('sale', 'Sales Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled'),
    ], string='Status', readonly=True, copy=False, index=True, tracking=3, default='draft')

    def compute_order_approval(self):
        '''
        Checks every order line, if finds a non-approved order line
        sets the order as not approved
        '''
        for sale in self:
            for line in sale.order_line:
                if not line.is_approved:
                    sale.is_approved = False
                    break
            else:
                sale.is_approved = True

    def action_quotation_reject(self):
        view = self.env.ref('log_wizard.log_message_wizard_view')
        wiz = self.env['log.message.wizard'].create({})
        model_description = self.type_name
        wiz_name = f"Reject {model_description}"
        wiz_subject = f"{model_description} rejected"

        ctx = {
            'subject': wiz_subject,
            'partner_ids': (self.user_id.partner_id.id,),
            'parent_model': self._name,
            'parent_id': self.id,
            'to_state': 'draft'
        }

        return {
            'name': wiz_name,
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'log.message.wizard',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'target': 'new',
            'res_id': wiz.id,
            'context': ctx
        }

    def action_ask_approval(self):
        all_users = self.env['res.users'].search([('active', '=', True)])

        # TODO: Specify managers depending on extra vendor discount

        if self.min_margin <= self.var_lvl_2_margin:
            my_users_group = all_users.filtered(lambda user: user.has_group(
                'ipx_sales_approval.ipx_sales_approval_manager'))
        else:
            my_users_group = all_users.filtered(lambda user: user.has_group(
                'ipx_sales_approval.ipx_sales_approval_assistant'))
        so_number = self.name

        order_id = self.id

        domain = self.env['ir.config_parameter'].sudo(
        ).get_param('web.base.url')

        url = f"{domain}/web#id={order_id}&action=334&model=sale.order&view_type=form&cids=1&menu_id=192"

        msg = f"<p>The Quotation {so_number} needs to be approved.</p>"

        for order in self:
            order.quote_margin_approved = self.approved_by_margin(order)
            order.quote_vendor_discount_approved = self.approved_by_extra_discount(
                order)

        if not self.quote_margin_approved:
            exceeded_items = []

            # Knowing which items are the reason for the approval
            for order in self:
                for line in order.order_line:
                    if line.real_margin <= line.min_appr_margin:
                        exceeded_items.append(
                            {'item': line.product_id.name, 'margin': (line.real_margin * 100)})

            msg += "<p>Items over the discount limit:</p><ul>"

            for item in exceeded_items:
                msg += f"<li>\t{item['item']} - Profit Margin: {round(item['margin'], 2)}%</li>"

            msg += "</ul>"

        if not self.quote_vendor_discount_approved:
            exceeded_items = []

            # Knowing which items are the reason for the approval
            for order in self:
                for line in order.order_line:
                    if line.extra_discount < line.vendor_discount or line.extra_discount > line.approved_extra_discount:
                        exceeded_items.append(
                            {'item': line.product_id.name, 'vendor_discount': (line.extra_discount * 100)})

            msg += "<p>Items with unapproved vendor discounts:</p><ul>"

            for item in exceeded_items:
                msg += f"<li>\t{item['item']} - Vendor Discount: {round(item['vendor_discount'], 2)}%</li>"

            msg += "</ul>"

        partner_ids = []
        for user in my_users_group:
            partner_ids.append(user.partner_id.id)

        self.message_post(
            subject='Quotation pending for Approval',
            body=msg,
            partner_ids=tuple(partner_ids)
            #             model=self._name,
            #             res_id=self.id
        )

        self.write({'state': 'to approve'})

    def action_quotation_approve(self):
        for line in self.order_line:
            line.approved_margin = line.get_profit_margin()

    is_approved = fields.Boolean(
        'Is Approved', store=True, compute='compute_order_approval')

    tmp_approve_level = fields.Integer('Approve level', default = 0)
            

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.depends('product_id', 'order_id.pricelist_id', 'order_id.partner_id')
    def compute_profit_margins(self):
        for line in self:
            line.default_margin = line.order_id.pricelist_id._get_default_margin(
                line.product_id)
            line.low_margin = line.order_id.pricelist_id._get_low_margin(
                line.product_id)
            line.min_margin = line.order_id.pricelist_id._get_min_margin(
                line.product_id)

    @api.depends('product_id', 'order_id.pricelist_id', 'order_id.partner_id', 'price_unit', 'margin_percentage')
    def compute_line_approved(self):
        for line in self:
            if line.num_profit_margin < line.approved_margin and line.num_profit_margin < line.low_margin:
                line.is_approved = False    
            else:
                line.is_approved = True
        
        tmp_approve_level = 0
        
        for line in self:
            if not line.is_approved:
                if line.num_profit_margin < line.min_margin and tmp_approve_level < 2:
                    tmp_approve_level = 2
                elif line.num_profit_margin < line.low_margin and tmp_approve_level < 1:
                    tmp_approve_level = 1
        
        self.order_id.approve_level = tmp_approve_level
            

    @api.depends('margin_percentage')
    def compute_numerical_profit_margin(self):
        for line in self:
            non_decimal = re.compile(r'[^\d.]+')
            line.num_profit_margin = float(non_decimal.sub('', line.margin_percentage)) or 0

    default_margin = fields.Float(
        'Default Profit Margin', store=True, compute='compute_profit_margins')
    low_margin = fields.Float(
        'Low Profit Margin', store=True, compute='compute_profit_margins')
    min_margin = fields.Float(
        'Minimum Profit Margin', store=True, compute='compute_profit_margins')

    approved_margin = fields.Float(
        'Approved Profit Margin', store=True, default= lambda self: self.default_margin)

    is_approved = fields.Boolean(
        'Is Validated', store=True, compute='compute_line_approved')

    num_profit_margin = fields.Float('Numerical Profit Margin', compute='compute_numerical_profit_margin')

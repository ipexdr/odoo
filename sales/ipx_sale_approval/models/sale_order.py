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

    @api.depends('order_line')
    def compute_order_approval(self):
        '''
        Checks every order line, if finds a non-approved order line
        sets the order as not approved
        '''
        _logger.info("computing order approval")
        for sale in self:
            for line in sale.order_line:
                if not line.is_approved and self.env['ir.config_parameter'].sudo().get_param('ipx_sale_approval.sales_order_approval_enabled'):
                    sale.is_approved = False
                    _logger.info("order not approved")
                    break
            else:
                sale.is_approved = True
                sale.state = 'draft'
                _logger.info("order approved")
        
        self.set_approval_level()

    def set_approval_level(self):
        # Setting order id approval level
        # 1 - Assistant
        # 2 - Manager

        tmp_approve_level = 0
        
        for line in self.order_line:
            if not line.is_approved:
                if line.profit_margin < line.default_margin:
                    tmp_approve_level = max(tmp_approve_level, 2)
                elif line.profit_margin < line.low_margin:
                    tmp_approve_level = max(tmp_approve_level, 1)
        
        self.approve_level = tmp_approve_level

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

        # Get all users from system
        all_users = self.env['res.users'].search([('active', '=', True)])
        
        if self.approve_level == 2:
            # Get users in approval manager group
            to_users = all_users.filtered(lambda user: user.has_group(
            'ipx_sale_approval.sales_approval_manager'))
        else:
            # Get users in approval manager assistant
            to_users =  all_users.filtered(lambda user: user.has_group(
            'ipx_sale_approval.sales_approval_assistant'))

            # Keep users that are not in approval manager group
            to_users = [user for user in to_users if user not in all_users.filtered(lambda user: user.has_group(
            'ipx_sale_approval.sales_approval_manager'))]
                
        partner_ids = []
        for user in to_users:
            # Getting users' partner ids
            partner_ids.append(user.partner_id.id)
        
        msg = f"<p>The Quotation {self.name} needs to be approved.</p>"

        exceeded_items = []

        # Knowing which items are the reason for the approval
        for line in self.order_line:
            if not line.is_approved:
                exceeded_items.append(
                    {'item': line.product_id.name, 'margin': (line.profit_margin)})

        msg += "<p>Items over the discount limit:</p><ul>"

        for item in exceeded_items:
            msg += f"<li>\t{item['item']} - Profit Margin: {round(item['margin'], 2)}%</li>"

        msg += "\n</ul>"

        self.message_post(
            subject='Quotation pending for Approval',
            body=msg,
            partner_ids=tuple(partner_ids)
        )

        self.write({'state': 'to approve'})

    def action_quotation_approve(self):
        for line in self.order_line:
            line.approved_margin = line.profit_margin

    is_approved = fields.Boolean(
        'Is Approved', store=True, compute='compute_order_approval')

    approve_level = fields.Integer('Approve level', default = 0)
            

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.depends('product_id', 'order_id.pricelist_id', 'order_id.partner_id')
    def _compute_low_margin(self):
        for line in self:
            line.low_margin = line.order_id.pricelist_id._get_low_margin(
                line.product_id)

    @api.depends('product_id', 'order_id.pricelist_id', 'order_id.partner_id', 'profit_margin', 'approved_margin')
    def _compute_line_approved(self):
        _logger.info("computing lines approval")
        for line in self:
            _logger.info(f"Profit margin - {line.profit_margin} | Approved margin - {line.approved_margin} | Low margin - {line.low_margin}")
            
            if line.profit_margin < line.approved_margin:
                line.is_approved = False
                
                _logger.info("Linea no aprobada")
            else:
                line.is_approved = True
                
                _logger.info("Linea aprobada")
        self.order_id.compute_order_approval()

    @api.depends('profit_margin')
    def _compute_profit_margin(self):
        for line in self:
            line.profit_margin = line.price_unit / line.product_id.standard_price - 1 if line.product_id.standard_price != 0 else 1

    low_margin = fields.Float(
        'Low Profit Margin', store=True, compute='_compute_low_margin')

    approved_margin = fields.Float(
        'Approved Profit Margin', store=True, default= lambda self: self.order_id.pricelist_id._get_default_margin(
                self.product_id))
    
    default_margin = fields.Float(
        'Approved Profit Margin', store=True, default= lambda self: self.order_id.pricelist_id._get_default_margin(
                self.product_id))

    is_approved = fields.Boolean(
        'Is Validated', store=True, compute='_compute_line_approved')

    profit_margin = fields.Float('Numerical Profit Margin', compute='_compute_profit_margin')

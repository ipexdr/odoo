# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = ['sale.order']

    min_margin = fields.Float(store=True, default=0.30, compute='compute_min_margin')
    quote_approved = fields.Boolean(store=True, default=True)

    quote_margin_approved = fields.Boolean(store=True, default=True)
    quote_vendor_discount_approved = fields.Boolean(store=True, default=True)

    var_lvl_1_margin = 0.20
    var_lvl_2_margin = 0.15
    std_min_margin = fields.Float(store=True, default=var_lvl_1_margin)

    # TODO: set default min_margin, var_lvl_1_margin from settings page

    # Overriding original state to add To Approve
    state = fields.Selection([
        ('draft', 'Quotation'),
        ('sent', 'Quotation Sent'),
        ('to approve', 'To Approve'),
        ('sale', 'Sales Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled'),
        ], string='Status', readonly=True, copy=False, index=True, tracking=3, default='draft')


    @api.depends('amount_total')
    def compute_min_margin(self):
        margins = []
        for order in self:
            for line in order.order_line:
                margins.append(line.real_margin)

        if len(margins) > 0:
            order.min_margin = min(margins)

    def action_ask_approval(self):
        all_users = self.env['res.users'].search([('active', '=', True)])

        # TODO: Specify managers depending on extra vendor discount

        if self.min_margin <= self.var_lvl_2_margin:
            my_users_group = all_users.filtered(lambda user: user.has_group('quote_fields.quote_fields_manager_2'))
        else:
            my_users_group = all_users.filtered(lambda user: user.has_group('quote_fields.quote_fields_manager_1'))
        so_number = self.name

        order_id = self.id

        domain = self.env['ir.config_parameter'].sudo().get_param('web.base.url')

        url = f"{domain}/web#id={order_id}&action=334&model=sale.order&view_type=form&cids=1&menu_id=192"

        msg = f"<p>The Quotation {so_number} needs to be approved.</p>"

        for order in self:
            order.quote_margin_approved = self.approved_by_margin(order)
            order.quote_vendor_discount_approved = self.approved_by_extra_discount(order)

        if not self.quote_margin_approved:
            exceeded_items = []

            # Knowing which items are the reason for the approval
            for order in self:
                for line in order.order_line:
                    if line.real_margin <= line.min_appr_margin:
                        exceeded_items.append({'item': line.product_id.name, 'margin': (line.real_margin * 100)})

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

        msg += f"<p>Click <a href=\"{url}\">here</a> to view the order."

        partner_ids = []
        for user in my_users_group:
            partner_ids.append(user.partner_id.id)

        self.message_notify(
            subject='Quotation pending for Approval',
            body=msg,
            partner_ids=tuple(partner_ids),
            model=self._name,
            res_id=self.id
        )

    def action_quotation_approve(self):
        for order in self:
            order.quote_approved = True
            for line in order.order_line:
                line.approved_extra_discount = line.extra_discount
                if line.real_margin < line.min_appr_margin:
                    line.min_appr_margin = line.real_margin

    def approved_by_margin(self, order):
        for line in order.order_line:
            if line.real_margin < line.min_appr_margin or line.real_margin < order.std_min_margin:
                return False
        return True

    def approved_by_extra_discount(self, order):
        for line in order.order_line:
            if line.extra_discount and line.extra_discount != line.vendor_discount:
                if line.extra_discount > line.approved_extra_discount or line.extra_discount < line.vendor_discount:
                    return False
        return True

    @api.onchange('amount_total')
    def set_approval(self):
        for order in self:
            _logger.info(f'Order no. {order.name}')
            order.quote_margin_approved = self.approved_by_margin(order)
            _logger.info(f"Margin approved - {order.quote_margin_approved}")
            order.quote_vendor_discount_approved = self.approved_by_extra_discount(order)
            _logger.info(f"Discount approved - {order.quote_vendor_discount_approved}")

            if order.quote_margin_approved and order.quote_vendor_discount_approved:
                self.quote_approved = True
            else:
                self.quote_approved = False
# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = ['sale.order']
    min_margin = fields.Float(store=True, default=0.30, compute='compute_min_margin')
    quote_approved = fields.Boolean(store=True, default=True)
    var_std_min_margin = 0.20
    std_min_margin = fields.Float(store=True, default=var_std_min_margin)

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

        if self.min_margin <= self.var_std_min_margin:
            my_users_group = all_users.filtered(lambda user: user.has_group('quote_fields.quote_fields_manager_2'))
        else:
            my_users_group = all_users.filtered(lambda user: user.has_group('quote_fields.quote_fields_manager_1'))
        so_number = self.name

        exceeded_items = []

        #       Knowing which items are the reason for the approval
        for order in self:
            for line in order.order_line:
                if line.real_margin <= line.min_appr_margin:

                    exceeded_items.append({'item': line.product_id.name, 'margin': (line.real_margin * 100)})

        order_id = self.id

        domain = self.env['ir.config_parameter'].sudo().get_param('web.base.url')

        url = f"{domain}/web#id={order_id}&action=321&model=sale.order&view_type=form&cids=1&menu_id=175"

        msg = f"<p>The Quotation {so_number} needs to be approved.</p><p>Items over the limit:</p><ul>"
        for item in exceeded_items:
            msg += f"<li>\t{item['item']} - Profit Margin: {item['margin']}%</li>"
        msg += f"</ul> <p>Click <a href=\"{url}\">here</a> to view the order."

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
                if line.real_margin < line.min_appr_margin:
                    line.min_appr_margin = line.real_margin

    @api.onchange('amount_total')
    def approved_by_margin(self):
        for order in self:
            for line in order.order_line:
                if line.real_margin < line.min_appr_margin or line.real_margin < order.std_min_margin:

                    order.quote_approved = False
                    break
                else:
                    order.quote_approved = True
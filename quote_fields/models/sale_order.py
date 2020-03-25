# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = ['sale.order']
    min_margin = fields.Float(store=True, default=0.30, compute='compute_min_margin')
    quote_approved = fields.Boolean(store=True, default=True)
    std_min_margin = fields.Float(store=True, default=0.20)

    @api.depends('amount_total')
    def compute_min_margin(self):
        margins = []
        for order in self:
            for line in order.order_line:
                new_margin = line.profit_margin - (line.price_unit * line.discount)
                new_margin = new_margin / line.price_unit
                margins.append(new_margin)

        for order in self:
            if margins:
                order.min_margin = min(margins)
            else:
                order.min_margin = 0.30

    def action_ask_approval(self):
        all_users = self.env['res.users'].search([('active', '=', True)])

        if self.max_discount >= 15:
            my_users_group = all_users.filtered(lambda user: user.has_group('quote_fields.quote_fields_manager_2'))
        else:
            my_users_group = all_users.filtered(lambda user: user.has_group('quote_fields.quote_fields_manager_1'))
        so_number = self.name

        exceeded_items = []

        #       Knowing which items are the resaon for the approval
        for order in self:
            for line in order.order_line:
                if line.discount > line.higher_disc:
                    exceeded_items.append({'item': line.product_id.name, 'discount_pct': line.discount})

        order_id = self.id
        domain = "ipexdr-so-approval-966903.dev.odoo.com"
        url = f"https://{domain}/web#id={order_id}&action=321&model=sale.order&view_type=form&cids=1&menu_id=175"

        msg = f"<p>The Quotation {so_number} needs to be approved.</p><p>Items over the limit:</p><ul>"
        for item in exceeded_items:
            msg += f"<li>\t{item['item']} - Discount: {item['discount_pct']}%</li>"
        msg += f"</ul> <p>Click <a href=\"{url}\">here</a> to view the order."

        partner_ids = []
        for user in my_users_group:
            partner_ids.append(user.partner_id.id)

        self.message_notify(
            subject='Quotation pending for Approval',
            body=msg,
            partner_ids=tuple(partner_ids)
        )

    def action_quotation_approve(self):
        for order in self:
            order.quote_approved = True
            for line in order.order_line:
                line.approved_disc = line.discount
                if line.discount > line.higher_disc:
                    line.higher_disc = line.discount

    @api.onchange('amount_total')
    def approved_by_discount(self):
        for order in self:
            for line in order.order_line:
                new_margin = line.profit_margin - (line.price_unit * line.discount)
                new_margin = new_margin / line.price_unit
                # if new_margin < order.min_margin
                if line.discount > line.approved_disc and line.discount > line.higher_disc:
                    order.quote_approved = False
                    break
                else:
                    order.quote_approved = True
# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = ['sale.order']
    quote_approved = fields.Boolean(store=True, string="Is approved", default=True)
    can_approve = fields.Boolean(compute="compute_can_approve")

    @api.onchange('amount_total')
    def compute_can_approve(self):
        lvl_2_discount = 15

        for order in self:
            for line in order.order_line:
                #                 ('quote_approved','=',True), ('state', '!=', 'draft'))
                if order.quote_approved == True or order.state != 'draft':
                    break
                else:
                    if (
                            lvl_2_discount > line.discount > line.higher_disc) and self.env.user.has_group(
                        'quote_fields.quote_fields_manager_1'):
                        order.can_approve = True
                    elif (
                            line.discount >= lvl_2_discount and line.discount > line.higher_disc) and self.env.user.has_group(
                        'quote_fields.quote_fields_manager_2'):
                        order.can_approve = True
                    else:
                        order.can_approve = False
                        break

    def action_ask_approval(self):
        all_users = self.env['res.users'].search([('active', '=', True)])

        my_users_group = all_users.filtered(lambda user: user.has_group('quote_fields.quote_fields_manager'))
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

    @api.depends('can_approve')
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
                if line.discount > line.approved_disc and line.discount > line.higher_disc:
                    order.quote_approved = False
                    break
                else:
                    order.quote_approved = True
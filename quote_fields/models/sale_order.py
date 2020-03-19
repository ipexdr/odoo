# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = ['sale.order']
    quote_approved = fields.Boolean(store=True, string="Is approved", default=True)

    def send_for_approval(self, recipients, message):
        self.message_notify(
            subject='Quotation pending for Approval',
            body=message,
            partner_ids=recipients,
        )

    #     TODO: action_ask_approval

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

                    _logger.info("Getting all users")
                    all_users = self.env['res.users'].search([('active', '=', True)])

                    _logger.info('Filtering users')
                    #                     my_users_group is type res.users list
                    my_users_group = all_users.filtered(
                        lambda user: user.has_group('quote_fields.quote_fields_manager'))
                    _logger.info(str(len(my_users_group)) + ' users found')
                    msg = "The Quotation SOXXXX is waiting for approval"

                    partner_ids = []
                    for user in my_users_group:
                        partner_ids.append(user.partner_id.id)

                    self.send_for_approval(tuple(partner_ids), msg)

                else:
                    order.quote_approved = True
# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    quote_approved = fields.Boolean(store=True, string="Is approved", default=True)

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


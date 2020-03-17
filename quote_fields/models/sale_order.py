# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    quote_approved = fields.Boolean(store=True, string="Is approved", default=True)
    pre_appr_disc = 5
    approved_disc = fields.Float(store=True, string="Approved Discount", default=5)

    def action_quotation_approve(self):
        for quote in self:
            quote.quote_approved = True

    @api.onchange('amount_total')
    def approved_by_discount(self):
        approved = True
        for order in self:
            for line in order.order_line:
                if line.discount > order.pre_appr_disc and line.discount > order.approved_disc:
                    approved = False
                    break
        for quote in self:
            quote.quote_approved = approved


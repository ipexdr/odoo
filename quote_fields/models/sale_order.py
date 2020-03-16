# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'
    quote_approved = fields.Boolean(store=True, string="Is approved", default=False)

    def action_quotation_approve(self):
        for quote in self:
            quote.approved = True
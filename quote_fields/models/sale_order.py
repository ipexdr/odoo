# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    state = fields.Selection(selection_add=[('quotation_approved', "Quotation Approved")])

    def action_quotation_approve(self):
        for quote in self:
            quote.state = 'quotation_approved'
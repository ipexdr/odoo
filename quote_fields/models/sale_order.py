# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    state = fields.Selection([
        ('draft', 'Quotation'),
        ('quotation_approved', "Quotation Approved"),
        ('sent', 'Quotation Sent'),
        ('sale', 'Sales Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled'),
    ], string='Status', readonly=True, copy=False, index=True, tracking=3, default='draft')

    #     state = fields.Selection(selection_add_after={'draft': [('quotation_approved', 'Quotation Approved')]})

    def action_quotation_approve(self):
        for quote in self:
            quote.state = 'quotation_approved'
# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleOrderLine(models.Model):
    _inherit = 'sale.order'

    state = fields.Selection(selection_add=[('quotation_approved', "Quotation Approved")])

    def action_quotation_approve(self):
        for line in self:
            line.state = 'quotation_approved'
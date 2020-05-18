# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    default_margin = 0.30
    min_appr_margin = fields.Float('Minimum Approved Margin', store=True, default=0.20)
    approved_extra_discount = fields.Float('Approved Vendor discount', default=0)
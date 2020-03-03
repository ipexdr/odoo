# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    # list_price = fields.Float('List Price', readonly=True, digits='Product Price', store=True)
    list_price = fields.Float('List Price', compute='_get_list_price', readonly=True, store=True)
    vendor_discount = fields.Float('Vendor Discount', store=True)
    vendor_discounted = fields.Float('Discounted', store=True)

    @api.depends('product_id')
    def _get_list_price(self):
        for line in self:
            line.list_price = line.product_id.standard_price

    @api.depends('vendor_discount')
    @api.onchange('vendor_discount')
    def _get_vendor_discount(self):
        for line in self:
            line.vendor_discounted = line.vendor_discount * line.list_price
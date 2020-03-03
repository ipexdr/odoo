# -*- coding: utf-8 -*-

from odoo import models, fields, api

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    # list_price = fields.Float('List Price', readonly=True, digits='Product Price', store=True)
    list_price = fields.Float('List Price')
    vendor_discount = fields.Float('Vendor Discount', widget='percentage')


    @api.depends('product_id')
    def _get_list_price(self):
        for record in self:
            record['list_price'] = record.product_id.standard_price




# class quote_fields(models.Model):
#     _name = 'quote_fields.quote_fields'
#     _description = 'quote_fields.quote_fields'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

# -*- coding: utf-8 -*-

from odoo import models, fields, api


# class SaleOrderInherit(models.Model):
#     _inherit = 'sale.order'


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    # list_price = fields.Float('List Price', readonly=True, digits='Product Price', store=True)
    list_price = fields.Char('List Price')

    # @api.depends('product_id')
    # def _get_list_price(self):
    #     for record in self:
    #         record.list_price = record.product_id.standard_price



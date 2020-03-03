# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    # list_price = fields.Float('List Price', readonly=True, digits='Product Price', store=True)
    list_price = fields.Float('List Price', compute='_get_list_price', readonly=True, store=True)
    vendor_discount = fields.Float('Vendor Discount', store=True)
    vendor_discounted = fields.Float('Discounted', store=True, readonly=True)
    # New
    fob_total = fields.Float('FOB Total', store=True, readonly=True)  # _get_fob_total
    tariff = fields.Float('Tariff', store=True)
    tariff_cost = fields.Float('Tariff Cost', store=True, readonly=True)  # _get_tariff_cost
    total_tariff_cost = fields.Float('Total Tariff Cost', store=True, readonly=True)  # _get_total_tariff_cost
    cost = fields.Float('Cost', store=True, readonly=True)  # _get_cost
    admin_cost = fields.Float('Admin. Cost', store=True)
    final_cost = fields.Float('Final Cost', store=True, readonly=True)  # _get_final_cost
    total_final_cost = fields.Float('Total Final Cost', store=True, readonly=True)  # _get_total_final_cost
    margin = fields.Float('Margin', store=True)
    profit_margin = fields.Float('Profit Margin', store=True, readonly=True)  # _get_profit_margin
    profit = fields.Float('Profit', store=True, readonly=True)  # _get_profit
    sell_price = fields.Float('Sell Price', store=True, readonly=True)  # _get_sell_price

    @api.depends('product_id')
    def _get_list_price(self):
        for line in self:
            line.list_price = line.product_id.standard_price

    @api.depends('vendor_discount')
    @api.onchange('vendor_discount')
    def _get_vendor_discount(self):
        for line in self:
            line.vendor_discounted = line.vendor_discount * line.list_price

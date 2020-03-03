# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    # list_price = fields.Float('List Price', readonly=True, digits='Product Price', store=True)
    list_price = fields.Float('List Price', compute='_get_list_price', readonly=True, store=True)
    vendor_discount = fields.Float('Vendor Discount', store=True)
    vendor_discounted = fields.Float('Discounted', store=True, readonly=True,
                                     compute='_get_vendor_discount')  # _get_vendor_discount | (Precio de lista) * (% Descuento fabricante)
    # New
    fob_total = fields.Float('FOB Total', store=True, readonly=True,
                             compute='_get_fob_total')  # _get_fob_total |  Precio de lista - Desc
    tariff = fields.Float('Tariff', store=True)
    tariff_cost = fields.Float('Tariff Cost', store=True, readonly=True)  # _get_tariff_cost | (Total FOB) * (% Arancel)
    total_tariff_cost = fields.Float('Total Tariff Cost', store=True,
                                     readonly=True)  # _get_total_tariff_cost | Costo de Arancel * Cantidad de Articulos
    cost = fields.Float('Cost', store=True, readonly=True)  # _get_cost | Total FOB + Costo de Arancel
    admin_cost = fields.Float('Admin. Cost', store=True)
    final_cost = fields.Float('Final Cost', store=True, readonly=True)  # _get_final_cost | Costo + Costo Adm
    total_final_cost = fields.Float('Total Final Cost', store=True,
                                    readonly=True)  # _get_total_final_cost | Costo Final x Cantidad
    margin = fields.Float('Margin', store=True)
    profit_margin = fields.Float('Profit Margin', store=True,
                                 readonly=True)  # _get_profit_margin | monto del % margen de ganancia
    profit = fields.Float('Profit', store=True, readonly=True)  # _get_profit | Margen G. * Cantidad
    sell_price = fields.Float('Sell Price', store=True, readonly=True)  # _get_sell_price | Costo Final + Margen G

    @api.depends('product_id')
    def _get_list_price(self):
        for line in self:
            line.list_price = line.product_id.standard_price

    @api.depends('vendor_discount')
    @api.onchange('vendor_discount')
    def _get_vendor_discount(self):
        """
        Compute the vendor discounted amount from vendor_discount
        :return:
        """
        for line in self:
            line.vendor_discounted = line.vendor_discount * line.list_price

    @api.depends('list_price', 'vendor_discounted')
    @api.onchange('vendor_discounted')
    def _get_fob_total(self):
        """
        Compute FOB Total amount from list_price - vendor_discounted
        :return:
        """
        for line in self:
            line.fob_total = line.list_price - line.vendor_discounted

    @api.depends('fob_total', 'tariff')
    def _get_tariff_cost(self):
        """
        Tariff Cost amount from FOB Total amount * Tariff percentage
        :return:
        """
        for line in self:
            line.tariff_cost = line.fob_total * line.tariff



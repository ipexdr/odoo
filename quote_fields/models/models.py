# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    # list_price = fields.Float('List Price', readonly=True, digits='Product Price', store=True)
    list_price = fields.Float('List Price', compute='_get_list_price', readonly=True, store=True)
    vendor_discount = fields.Float('Vendor Discount', store=True)
    vendor_discounted = fields.Float('Discounted', store=True, readonly=True,
                                     compute='_get_vendor_discount')  # (Precio de lista) * (% Descuento fabricante)
    # New
    fob_total = fields.Float('FOB Total', store=True, readonly=True,
                             compute='_get_fob_total')  # Precio de lista - Desc

    tariff = fields.Float('Tariff', store=True)
    tariff_cost = fields.Float('Tariff Cost', store=True, readonly=True)  # (Total FOB) * (% Arancel)
    total_tariff_cost = fields.Float('Total Tariff Cost', store=True,
                                     readonly=True)  # Costo de Arancel * Cantidad de Articulos

    cost = fields.Float('Cost', store=True, readonly=True)  # Total FOB + Costo de Arancel
    admin_cost = fields.Float('Admin. Cost', store=True, default=0)
    final_cost = fields.Float('Final Cost', store=True, readonly=True)  # Costo + Costo Adm
    total_final_cost = fields.Float('Total Final Cost', store=True,
                                    readonly=True)  # Costo Final x Cantidad

    margin = fields.Float('Margin', store=True) #  % de margen de ganancia aplicado al Costo Final
    profit_margin = fields.Float('Profit Margin', store=True,
                                 readonly=True)  # monto del % margen de ganancia
    profit = fields.Float('Profit', store=True, readonly=True)  # Margen G. * Cantidad
    sell_price = fields.Float('Sell Price', store=True, readonly=True)  # Costo Final + Margen G

    @api.depends('product_id')
    def _get_list_price(self):
        for line in self:
            line.list_price = line.product_id.standard_price

    @api.depends('vendor_discount')
    def _get_vendor_discount(self):
        """
        Compute the vendor discounted amount from vendor_discount
        :return:
        """

        for line in self:
            line.vendor_discounted = line.vendor_discount * line.list_price

    @api.depends('list_price', 'vendor_discounted')
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
        Total Tariff Cost from Tariff Cost * Quantity
        :return:
        """
        for line in self:
            line.tariff_cost = line.fob_total * line.tariff

    @api.depends('fob_total', 'tariff_cost')
    def _get_costs(self):
        for line in self:
            line.cost = line.fob_total + line.tariff_cost
            line.final_cost = line.admin_cost + line.cost
            line.total_final_cost = line.final_cost * line.product_uom_qty

    @api.depends('margin', 'profit_margin', 'final_cost')
    def _get_margin(self):
        for line in self:
            line.profit_margin = line.margin * line.final_cost
            line.profit = line.profit_margin * line.product_uom_qty
            line.sell_price = line.final_cost + line.profit_margin

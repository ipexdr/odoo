# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    default_margin = 0.30
    min_appr_margin = fields.Float('Minimum Approved Margin', store=True, default=0.20)

    list_price = fields.Float('List Price', compute='_compute_list_price', readonly=True, store=True)

    vendor_discount = fields.Float('Vendor Discount', store=True, default=0, compute='_compute_vendor_discount')

    extra_discount = fields.Float('Extra Vendor Discount', default=0)

    # TODO: _compute_new_discount
    #   - add extra_discount

    vendor_discounted = fields.Float('Discounted', store=True, readonly=True,
                                     compute='_compute_vendor_discounted')  # (Precio de lista) * (% Descuento fabricante)
    fob_total = fields.Float('FOB Total', store=True, readonly=True,
                             compute='_compute_fob_total')  # Precio de lista - Desc

    tariff = fields.Float('Tariff', store=True, default='0.08', compute='_compute_tariff')

    tariff_cost = fields.Float('Tariff Cost', store=True, readonly=True,
                               compute='_compute_tariff_cost')  # Get from Product (Total FOB) * (% Arancel)

    total_tariff_cost = fields.Float('Total Tariff Cost', store=True,
                                     readonly=True,
                                     compute='_compute_total_tariff_cost')  # Get from Product -  Costo de Arancel * Cantidad de Articulos

    cost = fields.Float('Cost', store=True, readonly=True, compute='_compute_cost')  # Total FOB + Costo de Arancel

    admin_cost = fields.Float('Admin. Cost', store=True, default=0)

    total_final_cost = fields.Float('Total Final Cost', store=True,
                                    readonly=True, compute='_compute_total_final_cost')  # Costo Final x Cantidad

    margin = fields.Float('Margin', store=True,
                          default=default_margin)  # % de margen de ganancia aplicado al Costo Final

    # Approval field

    real_margin = fields.Float('Real Margin', store=True, compute='_compute_real_margin', readonly=True,
                               default=default_margin)
    #   Approval field
    profit_margin = fields.Float('Profit Margin', store=True,
                                 readonly=True, compute='_compute_profit_margin')  # monto del % margen de ganancia
    profit = fields.Float('Profit', store=True, readonly=True, compute='_compute_profit')  # Margen G. * Cantidad
    sell_price = fields.Float('Sell Price', store=True, readonly=True,
                              compute='_compute_sell_price')  # Costo Final + Margen G

    # TODO: (??) change _compute_sell_price - get from product_id.list_price

    @api.depends('discount', 'cost', 'margin', 'profit_margin', 'sell_price')
    def _compute_real_margin(self):
        for line in self:
            if line.cost:
                new_margin = line.profit_margin - (line.sell_price * (line.discount * 0.01))
                line.real_margin = new_margin / line.cost
            else:
                line.real_margin = line.margin

    # @api.depends('product_id')
    # def _compute_admin_cost(self):
    #     for line in self:
    #         line.admin_cost = line.product_id.admin_fee

    @api.depends('product_id')
    def _compute_tariff(self):
        for line in self:
            line.tariff = (line.product_id.tariff * 0.01)

    @api.depends('product_id')
    def _compute_vendor_discount(self):
        for line in self:
            line.vendor_discount = (line.product_id.vendor_discount * 0.01)

    @api.depends('product_id')
    def _compute_list_price(self):
        for line in self:
            line.list_price = line.product_id.standard_price

    @api.depends('vendor_discount', 'list_price', 'extra_discount')
    def _compute_vendor_discounted(self):
        """
        Compute the vendor discounted amount from vendor_discount
        :return:
        """

        for line in self:
            if line.extra_discount and (line.extra_discount > line.vendor_discount):
                line.vendor_discounted = line.extra_discount * line.list_price
            else:
                line.vendor_discounted = line.vendor_discount * line.list_price

    @api.depends('list_price', 'vendor_discounted')
    def _compute_fob_total(self):
        """
        Compute FOB Total amount from list_price - vendor_discounted
        :return:
        """
        for line in self:
            line.fob_total = line.list_price - line.vendor_discounted

    @api.depends('fob_total', 'tariff')
    def _compute_tariff_cost(self):
        """
        Tariff Cost amount from FOB Total amount * Tariff percentage
        Total Tariff Cost from Tariff Cost * Quantity
        :return:
        """
        for line in self:
            line.tariff_cost = line.fob_total * line.tariff

    @api.depends('tariff_cost', 'product_uom_qty')
    def _compute_total_tariff_cost(self):
        """
        Tariff Cost amount from FOB Total amount * Tariff percentage
        Total Tariff Cost from Tariff Cost * Quantity
        :return:
        """
        for line in self:
            line.total_tariff_cost = line.tariff_cost * line.product_uom_qty

    @api.depends('fob_total', 'tariff_cost')
    def _compute_cost(self):
        for line in self:
            line.cost = line.fob_total + line.tariff_cost

    @api.depends('cost', 'product_uom_qty')
    def _compute_total_final_cost(self):
        for line in self:
            line.total_final_cost = (line.cost + line.admin_cost) * line.product_uom_qty

    @api.depends('margin', 'cost')
    def _compute_profit_margin(self):
        for line in self:
            line.profit_margin = line.margin * line.cost

    @api.depends('profit_margin', 'product_uom_qty')
    def _compute_profit(self):
        for line in self:
            line.profit = line.profit_margin * line.product_uom_qty

    @api.depends('profit_margin', 'cost', 'product_uom_qty')
    def _compute_sell_price(self):
        for line in self:
            line.sell_price = line.cost + line.profit_margin
            line.price_unit = line.sell_price

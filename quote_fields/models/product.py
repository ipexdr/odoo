# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)


class ProductTemplate(models.Model):
    _inherit = ['product.template']

    # overrided from product_template.py
    # list_price: catalog price, user defined
    list_price = fields.Float(
        'Sales Price', default=1.0,
        compute='_compute_list_price',
        digits='Product Price',
        help="Price at which the product is sold to customers.")

    default_margin = 30

    vendor_discount = fields.Float('Default Vendor Discount', store=True, default=0)

    # List price * (% vendor discount)
    vendor_discounted = fields.Float('Discounted', store=True, readonly=True,
                                     compute='_compute_vendor_discounted')
    # List price - discounted
    fob_total = fields.Float('FOB Total', store=True, readonly=True,
                             compute='_compute_fob_total')
    tariff = fields.Float('Tariff', store=True, default=8)

    # (Total FOB) * (% tariff)
    tariff_cost = fields.Float('Tariff Cost', store=True, readonly=True,
                               compute='_compute_tariff_cost')
    # Total FOB + tariff cost
    cost = fields.Float('Product Cost', store=True, readonly=True, compute='_compute_cost')
    admin_fee = fields.Float('Admin. Fee', store=True, default=0)
    #     final_cost = fields.Float('Final Cost', store=True, readonly=True,
    #                               compute='_compute_final_cost')

    margin = fields.Float('Margin', store=True,
                          default=default_margin, help='Default profit margin percentage')
    # profit margin real $amount (final cost * margin%)
    profit_margin = fields.Float(store=True,
                                 readonly=True, compute='_compute_profit_margin')

    @api.depends('fob_total', 'tariff_cost', 'admin_fee')
    def _compute_cost(self):
        """
        Calculates the product $cost by adding the total_fob, tariff $cost and admin fee
        """
        _logger.info("_compute_cost")
        for product in self:
            cost = product.fob_total + product.tariff_cost + product.admin_fee
            #             product.write({'cost':cost})
            product.cost = cost

    @api.depends('standard_price', 'vendor_discount')
    def _compute_vendor_discounted(self):
        """
        Calculates the discounted $amount from the list price (standard_price)
        using the vendor discount.
        :return:
        """
        _logger.info("compute_vendor_discounted")
        for product in self:
            vendor_discounted = product.standard_price * (product.vendor_discount * 0.01)
            #             product.write({'vendor_discounted': vendor_discounted})
            product.vendor_discounted = vendor_discounted

    @api.depends('vendor_discounted', 'standard_price')
    def _compute_fob_total(self):
        """
        Takes product's list price (standard_price) and subtracts
        the discounted $amount (vendor_discounted).
        :return:
        """
        _logger.info("_compute_fob_total")
        for product in self:
            fob_total = product.standard_price - product.vendor_discounted
            #             product.write({'fob_total': fob_total})
            product.fob_total = fob_total

    @api.depends('tariff', 'fob_total')
    def _compute_tariff_cost(self):
        """
        Calculates tariff real $amount from tariff and fob_total fields
        :return:
        """
        _logger.info("_compute_tariff_cost")

        for product in self:
            tariff_cost = (product.tariff * 0.01) * product.fob_total
            #             product.write({'tariff_cost': tariff_cost})
            product.tariff_cost = tariff_cost

    #     @api.depends('admin_fee', 'cost')
    #     def _compute_final_cost(self):
    #         """
    #         Adds admin_fee and cost, to get final_cost value.
    #         Final_cost value will be used to calculate the final Sale Price
    #         :return:
    #         """
    #         for product in self:
    #             final_cost = product.admin_fee + product.cost
    # #             product.write({'final_cost': final_cost})
    #             product.final_cost = final_cost

    @api.depends('margin', 'cost')
    def _compute_profit_margin(self):
        """
        Computes product's profit margin $amount from the final cost and
        margin pct%

        profit_margin = cost * margin
        :return:
        """
        _logger.info("_compute_profit_margin")

        for product in self:
            profit_margin = product.cost * (product.margin * 0.01)
            product.profit_margin = profit_margin

    @api.depends('cost', 'margin')
    def _compute_list_price(self):
        """
        Each time the cost or margin is affected, applies the
        corresponding price to the product's sale price
        :return:
        """
        _logger.info("_compute_list_price")

        for product in self:
            sale_price = product.cost + product.profit_margin
            product.list_price = sale_price

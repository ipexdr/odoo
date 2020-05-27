# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = ['sale.order']

    full_discount = fields.Float(store=True, default=0, string="Quotation Discount (%)")
    quote_discounted = fields.Float(string="Discounted Amount", compute='_compute_quote_discount')
    undiscounted_total = fields.Float()

    @api.depends('full_discount', 'amount_total')
    def _compute_quote_discount(self):
        """
        Compute the SO's general discount
        """
        for order in self:
            if order.full_discount:
                order.quote_discounted = order.amount_total * (order.full_discount * 0.01)
            else:
                order.quote_discounted = 0
    
    @api.depends('order_line.price_total', 'quote_discounted')
    def _amount_all(self):
        """
        Compute the total amounts of the SO.
        """
        for order in self:
            amount_untaxed = amount_tax = 0.0
            for line in order.order_line:
                amount_untaxed += line.price_subtotal
                amount_tax += line.price_tax
            order.update({
                'amount_untaxed': amount_untaxed,
                'amount_tax': amount_tax,
                'amount_total': (amount_untaxed + amount_tax) - order.quote_discounted,
                'undiscounted_total': amount_untaxed + amount_tax,
            })
# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = ['sale.order']

    full_discount = fields.Float(store=True, default=0, string="Quotation Discount (%)")

    @api.onchange('full_discount')
    def _set_full_discount(self):
        for order in self:
            for line in order.order_line:
                if order.full_discount:
                    # If full discount != 0, each empty
                    # discount field will be = full discount
                    if not line.discount:
                        line.discount = order.full_discount
                else:
                    # In case full discount == 0, then
                    # every discount field = 0
                    line.discount = 0
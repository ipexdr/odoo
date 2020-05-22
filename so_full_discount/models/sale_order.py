# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = ['sale.order']

    full_discount = fields.Float(store=True, default=0, string="Quotation Discount (%)")

    @api.depends('full_discount')
    def _set_full_discount(self):
        for order in self:
            for line in order.order_line:
                if not line.discount:
                    line.discount = line.full_discount
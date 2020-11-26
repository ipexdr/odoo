# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.depends('product_id', 'order_id.pricelist_id', 'order_id.partner_id')
    def compute_profit_margins(self):
        for line in self:
            line.default_margin = line.order_id.pricelist_id._get_default_margin(
                line.product_id)
            line.low_margin = line.order_id.pricelist_id._get_low_margin(
                line.product_id)
            line.min_margin = line.order_id.pricelist_id._get_min_margin(
                line.product_id)
    

    default_margin = fields.Float(
        'Default Profit Margin', store=True, compute='compute_profit_margins')
    low_margin = fields.Float(
        'Low Profit Margin', store=True, compute='compute_profit_margins')
    min_margin = fields.Float(
        'Minimum Profit Margin', store=True, compute='compute_profit_margins')

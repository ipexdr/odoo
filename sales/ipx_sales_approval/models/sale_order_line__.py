# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging, re

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
    
    @api.depends('product_id', 'order_id.pricelist_id', 'order_id.partner_id', 'price_unit')
    def compute_line_validation(self):
        non_decimal = re.compile(r'[^\d.]+')
        for line in self:
            profit_margin =  float(non_decimal.sub('', line.margin_percentage))
            if profit_margin < line.approved_margin:
                line.is_validated = False
            else:
                line.is_validated = True

    default_margin = fields.Float(
        'Default Profit Margin', store=True, compute='compute_profit_margins')
    low_margin = fields.Float(
        'Low Profit Margin', store=True, compute='compute_profit_margins')
    min_margin = fields.Float(
        'Minimum Profit Margin', store=True, compute='compute_profit_margins')

    approved_margin = fields.Float('Approved Profit Margin', store=True, default=default_margin)

    is_validated = fields.Booelan('Is Validated', store=True, compute='compute_line_validation')
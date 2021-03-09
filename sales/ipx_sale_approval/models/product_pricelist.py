# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.tools.profiler import profile
import logging

_logger = logging.getLogger(__name__)


class PriceList(models.Model):
    _inherit = 'product.pricelist'
        
    def _get_low_margin(self, product):
        for item in self.item_ids:
            if (item.applied_on == '0_product_variant' and item.product_id == product) or (item.applied_on == '1_product' and item.product_tmpl_id == product.product_tmpl_id) or(item.applied_on == '2_product_category' and item.categ_id == product.categ_id) or item.applied_on == '3_global':
                return item.low_margin
        else:
            return 0

    def _get_default_margin(self, product):
        for item in self.item_ids:
            if (item.applied_on == '0_product_variant' and item.product_id == product) or (item.applied_on == '1_product' and item.product_tmpl_id == product.product_tmpl_id) or(item.applied_on == '2_product_category' and item.categ_id == product.categ_id) or item.applied_on == '3_global':
                _logger.info(f"Default margin {item.default_margin}")
                return item.default_margin
        else:
            return 0

class PricelistItem(models.Model):
    _inherit = 'product.pricelist.item'

    @api.depends('price_discount')
    def _compute_default_margin(self):
        for item in self:
            item.default_margin = item.price_discount * -1

    default_margin = fields.Float('Default Profit Margin', store=True, compute="_compute_default_margin")
    low_margin = fields.Float('Low Profit Margin', store=True, default=0)
# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.tools.profiler import profile
import logging

_logger = logging.getLogger(__name__)


class PriceList(models.Model):
    _inherit = 'product.pricelist'

    def _get_default_margin(self, product):
        for item in self.item_ids:
            if item.applied_on == '2_product_category' and item.categ_id == product.categ_id:
                return item.default_margin
        else:
            return 0
        
    def _get_low_margin(self, product):
        for item in self.item_ids:
            if item.applied_on == '2_product_category' and item.categ_id == product.categ_id:
                return item.low_margin
        else:
            return 0
        
    def _get_min_margin(self, product):
        for item in self.item_ids:
            if item.applied_on == '2_product_category' and item.categ_id == product.categ_id:
                return item.min_margin
        else:
            return 0

class PricelistItem(models.Model):
    _inherit = 'product.pricelist.item'

    default_margin = fields.Float('Default Profit Margin', store=True, default=0)
    low_margin = fields.Float('Low Profit Margin', store=True, default=0)
    min_margin = fields.Float('Minimum Profit Margin', store=True, default=0)
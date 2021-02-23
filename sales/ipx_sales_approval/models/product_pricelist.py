# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.tools.profiler import profile
import logging

_logger = logging.getLogger(__name__)


class PriceList(models.Model):
    _inherit = 'product.pricelist'
        
    def _get_low_margin(self, product):
        for item in self.item_ids:
            if item.applied_on == '2_product_category' and item.categ_id == product.categ_id:
                return item.low_margin
        else:
            return 0

class PricelistItem(models.Model):
    _inherit = 'product.pricelist.item'

    def _compute_default_margin(self):
        for item in self:
            item.default_margin = item.price_discount * -1

    default_margin = fields.Float('Default Profit Margin', store=True, compute="_compute_default_margin")
    low_margin = fields.Float('Low Profit Margin', store=True, default=0)
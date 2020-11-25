# -*- coding: utf-8 -*-
from odoo import models, fields, api


class PriceList(models.Model):
    _inherit = 'product.pricelist'

    def _get_default_margin(self, product):
        for item in self.item_ids:
            if item.applied_on == '3_product_category' and item.categ_id == product.categ_id:
                return item.default_margin
        else:
            return 0

class PricelistItem(models.Model):
    _inherit = 'product.pricelist.item'

    default_margin = fields.Float('Default Profit Margin', store=True, default=0)
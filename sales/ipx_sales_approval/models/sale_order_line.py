# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    def _get_default_margin(self, product):
        for line in self:
            return line.order_id.pricelist_id._get_default_margin(line.product_id)            

    default_margin = fields.Float('Default Profit Margin', store=True, default='_get_default_margin()')
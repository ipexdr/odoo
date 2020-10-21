# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)


class ProductTemplate(models.Model):
    _inherit = ['product.template']

    vendor_discount = fields.Float('Default Vendor Discount', store=True, default=30)

    tariff = fields.Float('Tariff', store=True, default=8)
    
    # Total FOB + tariff cost
    vendor_list_price = fields.Float('List Price', store=True, default=1)
    # admin_fee = fields.Float('Admin. Fee', store=True, default=0)
    #     final_cost = fields.Float('Final Cost', store=True, readonly=True,
    #                               compute='_compute_final_cost')

    margin = fields.Float('Margin', store=True,
                          default=30)

    manufacturer = fields.Char(store=True)
    
    real_margin = fields.Float('Real Margin', store=True, help='Real computed profit margin', compute='_compute_real_margin')

    @api.depends('list_price', 'standard_price')
    def _compute_real_margin(self):
        """
        Computes product's profit margin $amount from the final cost and
        margin pct%
        profit_margin = standard_price * margin
        :return:
        """
        for template in self:
            template.real_margin = ((template.list_price - template.standard_price) / template.standard_price) * 100 if template.standard_price else 0


        
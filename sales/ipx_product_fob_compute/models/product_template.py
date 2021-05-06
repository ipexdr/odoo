# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)


class ProductTemplate(models.Model):
    _inherit = ['product.template']
    
    tariff = fields.Float('Tariff', store=True, default=30)
    exprected_listprice = fields.Float('Expected price', store=False)
    
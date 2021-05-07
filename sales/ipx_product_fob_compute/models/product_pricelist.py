# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)


class Pricelist(models.Model):
    _inherit = ['product.pricelist']
    
    
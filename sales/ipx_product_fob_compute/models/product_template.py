# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)


class ProductTemplate(models.Model):
    _inherit = ['product.template']
    

    tariff_opts = [('', 'No Tariff'), ('categ_tariff', 'Category Tariff'), ('custom_tariff', 'Custom Tariff')]
    select_tariff = fields.Selection(tariff_opts, string="Tariff", default='')

    default_tariff = fields.Float('Tariff Percentage', related='categ_id.default_tariff')
    custom_tariff = fields.Float('')
    
    expected_listprice = fields.Float('Expected price', store=True)

    @api.model_create_multi
    def create(self, vals):
        templates = super(ProductTemplate, self).create(vals)
        for template in templates:
            if template.categ_id.default_tariff:
                template.tariff_opts = 'categ_tariff'
            # if template.tariff_opts != 'custom_tariff':
            #     if template.categ_id.has_tariff:
            #         tariff_opts = 'categ_tariff'

        return templates

    # TODO: Compute price from tariff in template or categ
    # def _compute_expected_listprice(self):
    #     for template in self:
    #         if 
    
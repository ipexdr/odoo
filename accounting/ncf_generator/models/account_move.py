# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
import logging

_logger = logging.getLogger(__name__)

class AccountMove(models.Model):
    _inherit = ['account.move']
    
    NFC_TYPES = [
        ('gasto_menor', 'Gasto Menor'),
        ('prov_informal', 'Proveedor Informal'),
        ('cons_final', 'Consumidor Final'),
        ('gubernamental', 'Gubernamental'),
        ('reg_especal', 'Regimen Especial'),
        ('credito_fiscal', 'Credito Fiscal'),
        ('nota_credito', 'Nota Credito'),
        ('nota_debito', 'Nota Debito')
    ]
    
    ncf = fields.Char('NCF')
    ncf_type = fields.Selection(NFC_TYPES, string='NCF Type')
    
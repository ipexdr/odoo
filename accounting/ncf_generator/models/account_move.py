# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
import logging
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)

class AccountMove(models.Model):
    _inherit = ['account.move']

    def set_ncf(self, ncf_type):
        for move in self:
            ncf = self.env['ir.sequence'].get(move.ncf_type)
            return ncf
        
    def default_ncf_type(self, ncf_types):
        return ncf_types[0][0]
    
    def get_ncf(self, ncf_type):
        for move in self:
            sequence = self.env['ir.sequence'].search([('code','=',move.ncf_type)])
            ncf = sequence.get_next_char(sequence.number_next_actual)
            return ncf
        
    @api.constrains('ncf')
    def _check_ncf_length(self):
        if len(self.ncf) in range(1, 11):
           raise ValidationError('NCF is shorter than 11 characters')
        elif len(self.ncf) > 11:
           raise ValidationError('NCF is longer than 11 characters')
    
    @api.onchange('ncf_type')
    def change_ncf(self):
        for move in self:
            move.ncf = self.get_ncf(move.ncf_type)
    
    #TODO: Depends on ncf_type to change ncf
    #TODO: [no priority] Depends on ncf to change type
    
    NCF_TYPES = [
        ('ncf.gasto.menor', 'Gasto Menor'),
        ('ncf.prov.informal', 'Proveedor Informal'),
        ('ncf.con.final', 'Consumidor Final'),
        ('ncf.gubernamental', 'Gubernamental'),
        ('ncf.reg.especial', 'Regimen Especial'),
        ('ncf.credito.fiscal', 'Credito Fiscal'),
        ('ncf.nota.credito', 'Nota Credito'),
        ('ncf.nota.debito', 'Nota Debito')
    ]
    
    ncf = fields.Char('NCF', default='', size=11)
    ncf_type = fields.Selection(NCF_TYPES, string='NCF Type', default=NCF_TYPES[0][0])
    
    # TODO: On write method to affect the sequence
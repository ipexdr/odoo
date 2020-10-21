# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
import logging

_logger = logging.getLogger(__name__)

class AccountMove(models.Model):
    _inherit = ['account.move']
    
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
    
    ncf = fields.Char('NCF')
    ncf_type = fields.Selection(NCF_TYPES, string='NCF Type')
    
    @api.onchange('ncf_type')
    def change_ncf(self):
        for move in self:
            if move.ncf_type:
                # Takes next sequence value without affecting the sequence counter
                sequence = self.env['ir.sequence'].search([('code','=',move.ncf_type)])
                next = sequence.get_next_char(sequence.number_next_actual) or ''
                move.write({'ncf': next})
            else:
                move.write({'ncf': ''})

    # on create method
    @api.model
    def create(self, vals):
        move = super(AccountMove, self).create(vals)
        if move.ncf_type and move.ncf:
            sequence = self.env['ir.sequence'].search([('code','=',move.ncf_type)])
            # Applies the sequence value and adds to the sequence counter
            if move.ncf == sequence.get_next_char(sequence.number_next_actual):
                self.env['ir.sequence'].get(move.ncf_type)
            
        return move

# TODO: On write method
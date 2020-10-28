# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
import logging
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)

class AccountMove(models.Model):
    _inherit = ['account.move']

    def set_ncf(self):
        for move in self:
            ncf = move.env['ir.sequence'].next_by_code(move.ncf_type)
            return ncf
        
    def default_ncf_type(self, ncf_types):
        return ncf_types[0][0]
    
    def get_ncf(self):
        for move in self:
            sequence = move.env['ir.sequence'].search([('code','=',move.ncf_type)])
            ncf = sequence.get_next_char(sequence.number_next_actual)
            return ncf
        
    @api.constrains('ncf')
    def _check_ncf_length(self):
        for move in self:
            if len(move.ncf) in range(1, 11):
                raise ValidationError('NCF is shorter than 11 characters')
            elif len(move.ncf) > 11:
                raise ValidationError('NCF is longer than 11 characters')
    
    @api.constrains('ncf')
    def _check_unique_ncf(self):
        for move in self:
            if move.ncf:
                # Getting all the invoices (hopefully 1) with the same ncf
                invoices = self.env['account.move'].search([('ncf','=',move.ncf)])
                
                if len(invoices) > 1:
                    error_text = f"NCF {move.ncf} is already taken by {len(invoices)-1} invoice(s).\n"
                    
                    # Getting invoices attributes to show as a description in Exception window
                    for invoice in invoices[1:]:
                        
                        inv_name = invoice.name if invoice.name != '/' else "Unposted invoice"
                        inv_partner = invoice.partner_id.name if invoice.partner_id.name else "No partner assigned"
                        inv_date = invoice.date if invoice.date else "No date assigned"
                        
                        error_text += f"- {inv_name} | {inv_partner} | {inv_date}\n"
                    raise ValidationError(error_text)
    
    @api.onchange('ncf_type')
    def change_ncf(self):
        for move in self:
            move.ncf = self.get_ncf()
            
    @api.model
    def create(self, values):
        """Override default Odoo create function and extend."""
        move = super(AccountMove, self).create(values)
        if move.ncf == move.get_ncf():
            move.set_ncf()
        return move
    
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
    ncf_type = fields.Selection(NCF_TYPES, string='NCF Type', default='')
    
    # TODO: On write method to affect the sequence
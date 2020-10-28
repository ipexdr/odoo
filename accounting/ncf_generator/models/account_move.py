# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
import logging
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)

class AccountMove(models.Model):
    _inherit = ['account.move']

    def _get_ncf_types(self):
        records = self.env['ncf_generator.ncf_sequence'].search()
        ncf_types = [('', 'N/A')]
        for record in records:
            ncf_types.append((record.code, record.name))
        return ncf_types

    def set_ncf(self):
        for move in self:
            ncf = self.env['ncf_generator.ncf_sequence'].next_by_code(move.ncf_type)
            return ncf
        
    def default_ncf_type(self, ncf_types):
        return ncf_types[0][0]
    
    def get_ncf(self):
        for move in self:
            sequence = self.env['ncf_generator.ncf_sequence'].search([('code','=',move.ncf_type)])
            ncf = sequence.get_next_char(sequence.number_next_actual)
            return ncf
        
    @api.constrains('ncf')
    def _check_ncf_length(self):
        for move in self:
            if move.ncf:
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
            if move.ncf_type:
                move.ncf = move.get_ncf()
            else:
                move.ncf = ''
            
    @api.model
    def create(self, values):
        """Override default Odoo create function and extend."""
        move = super(AccountMove, self).create(values)
        if move.ncf_type and (move.ncf == move.get_ncf()):
            move.set_ncf()
        return move
    
    ncf = fields.Char('NCF', default='', size=11)
    ncf_type = fields.Selection(_get_ncf_types, string='NCF Type', default='')
    
    # TODO: On write method to affect the sequence
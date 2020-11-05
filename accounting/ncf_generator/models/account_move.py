# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
import logging
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)

class AccountMove(models.Model):
    _inherit = ['account.move']
    
    @api.depends('type')
    def _get_ncf_types_domain(self):
        for move in self:
            _logger.info(f"GETTING DOMAIN FOR {move.type}")
            domain = [('id', '=', -1)]
            final_ncf_types = []
            ncf_types = move.env['ir.sequence'].search([('is_ncf','=',True)])
            _logger.info(f"found ncf types -> {[ncf_type.name for ncf_type in ncf_types]}")
            for ncf_type in ncf_types:
                if move.type in [move_type.code for move_type in ncf_type.move_type_ids]:
                    final_ncf_types.append(ncf_type.id)
            _logger.info(f"final ncf types -> {final_ncf_types}")
            if final_ncf_types:
                move.ncf_type_list = final_ncf_types
    
    def get_ncf(self):
        for move in self:
#             _logger.info(f"Move's ncf_€type var -> {move.ncf_type}")
            sequence = move.ncf_type
            ncf = sequence.get_next_char(sequence.number_next_actual)
            return ncf
        
    def set_ncf(self):
        for move in self:
            ncf = self.env['ir.sequence'].next_by_code(move.ncf_type.code)
            return ncf
        
    @api.constrains('ncf')
    def _check_ncf_length(self):
        for move in self:
            if move.ncf:
                if len(move.ncf) in range(1, 11):
#                     _logger.info(f"NCF => {move.ncf}")
                    raise ValidationError('NCF is shorter than 11 characters')
                elif len(move.ncf) > 11:
#                     _logger.info(f"NCF => {move.ncf}")
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
    
#     TODO: Set ncf and ncf_type as available only in states other than draft
    
    ncf = fields.Char('NCF', default='', size=11)
    ncf_type_list = fields.Many2many('ir.sequence',store=True,compute=_get_ncf_types_domain)   # Avaliable ncf types according to the move type
    ncf_type = fields.Many2one('ir.sequence', string='NCF Type')

# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
import logging
# from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)

class NcfSequence(models.Model):
    _name = 'ncf_generator.ncf_sequence'
    _inherit = ['ir.sequence']
    _description = 'NCF Sequence'
    _order = 'name'

    
    move_type_ids = fields.Many2many('ncf_generator.move_type', string="Move Types")
    due_date = fields.Date(string='Due Date', default=fields.Date.context_today)
    number_last = fields.Integer('Last Number')
# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
import logging
# from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class IrSequence(models.Model):
    _inherit = ['ir.sequence']

    is_ncf = fields.Boolean(default=False)
    move_type_ids = fields.Many2many(
        'ncf_generator.move_type', string="Move Types")
    due_date = fields.Date(
        string='Due Date', default=fields.Date.context_today)
    number_last = fields.Integer('Last Number')

# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
import logging
# from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)

class MoveType(models.Model):
    _name = 'ncf_generator.move_type'
    _description = 'Move Type'
    _order = 'name'

    name = fields.Char("Name")
    code = fields.Char("Code")
    
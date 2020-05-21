# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import AccessError, UserError, ValidationError
import logging

_logger = logging.getLogger(__name__)

class Project(models.Model):
    _inherit = 'project.project'
    stage_id = fields.Many2one('project.task.type', string='Stage', ondelete='restrict', tracking=True, index=True,
        default=_get_default_stage_id, group_expand='_read_group_stage_ids', copy=False)

class Task(models.Model):
    _inherit = "project.task"

    iteration = fields.Char(string='Iteration', tracking=True)
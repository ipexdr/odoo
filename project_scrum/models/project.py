# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import AccessError, UserError, ValidationError
import logging

_logger = logging.getLogger(__name__)


class ProjectStage(models.Model):
    _name = 'project.stage'
    _description = 'Project Stage'
    _order = 'id'

    name = fields.Char('Stage Name')

class Project(models.Model):
    _inherit = 'project.project'
    stage_id = fields.Many2one('project.stage', string='Stage', ondelete='restrict', tracking=True, index=True,
    copy=False)


class Task(models.Model):
    _inherit = "project.task"

    iteration = fields.Char(string='Iteration', tracking=True)
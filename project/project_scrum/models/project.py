# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import AccessError, UserError, ValidationError
import logging

_logger = logging.getLogger(__name__)


class ProjectStage(models.Model):
    _name = 'project.stage'
    _description = 'Project Stage'
    _order = 'sequence, id'
    
    sequence = fields.Integer(default=1)
    name = fields.Char('Stage Name')
    fold = fields.Boolean('Folded', default=False)
    description = fields.Text()

class Project(models.Model):
    _inherit = 'project.project'
    
    @api.model
    def _read_group_stage_ids(self, stages, domain, order):
        stage_ids = self.env['project.stage'].search([])
        return stage_ids
    
    stage_id = fields.Many2one('project.stage', tracking=True, string='Stage', ondelete='restrict', index=True,
    copy=False, group_expand='_read_group_stage_ids')


class Task(models.Model):
    _inherit = "project.task"

    iteration = fields.Char(string='Iteration', tracking=True)
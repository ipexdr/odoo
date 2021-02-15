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
    iteration_template = fields.Many2one('project.iteration.template', string='Iteration Template')
    
class Task(models.Model):
    _inherit = "project.task"

    iteration = fields.Char('Iteration', tracking=True)
    iteration_id = fields.Many2one('project.iteration', string='Iteration')

class Iteration(models.Model):
    _inherit = 'project.iteration'
    
    start_date = fields.date("Fecha Inicio", default=fields.Date.context_today)
    end_date = fields.date("Fecha Inicio", default=fields.Date.context_today)
    
    iteration_template_id = fields.Many2one('project.iteration.template', string='Iteration Template')
    
    display_name = fields.char('Iteration name')

class IterationTemplates(models.Model):
    _inherit = 'project.iteration.template'
    
    iteration_length = fields.Int('Iteration Length (days)', default=5)
    display_name = fields.Char('Iteration Template Name')

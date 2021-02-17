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

    iteration = fields.Char('Iteration (str)', tracking=True)
    iteration_id = fields.Many2one('project.iteration', string='Iteration')

class Iteration(models.Model):
    _name = 'project.iteration'
    _description = 'Iteration'
    
    start_date = fields.Date("Start Date", default=fields.Date.context_today)
    end_date = fields.Date("End Date", default=fields.Date.context_today)
    
    iteration_template_id = fields.Many2one('project.iteration.template', string='Iteration Template')
    
    display_name = fields.Char('Iteration name')

class IterationTemplate(models.Model):
    _name = 'project.iteration.template'
    _description = 'Iteration Template'
    
    def name_get(self):
        res = []
        for template in self:
            res.append((template.id, template.display_name))
        return res
    
    iteration_length = fields.Integer('Iteration Length (days)', default=5)
    first_iteration_date = fields.Date('First Iteration')
    display_name = fields.Char('Iteration Template Name')

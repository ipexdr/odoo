# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import AccessError, UserError, ValidationError
from dateutil.relativedelta import relativedelta
from datetime import datetime
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
    
    def name_get(self):
        res = []
        for iteration in self:
            res.append((iteration.id, iteration.display_name))
        return res
    
    @api.depends('iteration_template_id', 'start_date')
    def _compute_display_name(self):
        for iteration in self:
            iteration.display_name = f"{iteration.start_date} | {iteration.end_date}"

    @api.depends('iteration_template_id', 'start_date')
    def _compute_end_date(self):
        for iteration in self:
            iteration_template_days = iteration.iteration_template_id.iteration_length
            iteration.end_date = iteration.start_date + relativedelta(days = iteration_template_days)
    
    start_date = fields.Date("Start Date", default=fields.Date.context_today, required=True)
    end_date = fields.Date("End Date", default=fields.Date.context_today, compute='_compute_end_date')
    
    iteration_template_id = fields.Many2one('project.iteration.template', string='Iteration Template', required=True)
    
    display_name = fields.Char('Iteration name')

class IterationTemplate(models.Model):
    _name = 'project.iteration.template'
    _description = 'Iteration Template'
    
    @api.model
    def create(self, values):
        new_date = values['first_iteration_date']
        res = super(IterationTemplate, self).create(values)
        for i in range(4):
            new_vals = {
                'start_date':new_date,
                'iteration_template_id':res.id
            }
            self.env['project.iteration'].create(new_vals)
            new_date = res.first_iteration_date + relativedelta(days = res.iteration_length)
            
        return res
    
    def name_get(self):
        res = []
        for template in self:
            res.append((template.id, template.display_name))
        return res

    @api.depends('iteration_length')
    def _compute_display_name(self):
        for template in self:
            template.display_name = f"{template.iteration_length}-Day iteration"
    
    iteration_length = fields.Integer('Iteration Length (days)', default=5, required=True)
    first_iteration_date = fields.Date('First Iteration', required=True)
    display_name = fields.Char('Iteration Template Name', compute='_compute_display_name')

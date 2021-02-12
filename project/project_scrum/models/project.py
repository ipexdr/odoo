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

class Iteration(models.Model):
    _inherit = 'project.iteration'
    
    fecha_inicio = fields.date([
        ('date', 'BeginningDate'),
        ('datetime', 'BeginningDatetime')], string="Fecha Inicio", default='date')
    fecha_final = fields.date([
        ('date', 'FinalDate'),
        ('datetime', 'FinalDatetime')], string="Fecha Final", default='date')
    display_name = fields.char('iteracion name')

class IterationTemplates(models.Model):
    _inherit = 'project.iterationtemplates'
    
    fecha_inicio = fields.date([
        ('date', 'BeginningDate'),
        ('datetime', 'BeginningDatetime')], string="Fecha Inicio", default='date')
    fecha_final = fields.date([
        ('date', 'FinalDate'),
        ('datetime', 'FinalDatetime')], string="Fecha Final", default='date')
    display_name = fields.char('iteraciontemplate name')
    

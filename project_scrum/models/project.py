# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import AccessError, UserError, ValidationError
import logging

_logger = logging.getLogger(__name__)


class Project(models.Model):
    _inherit = 'project.project'
    stage = fields.Selection([
        ('to do', 'To Do'),
        ('in progress', 'In Progress'),
        ('done', 'Done')
    ],
    string="Stage", default="to do", required=True)


class Task(models.Model):
    _inherit = "project.task"

    iteration = fields.Char(string='Iteration', tracking=True)
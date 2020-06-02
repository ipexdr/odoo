# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import AccessError, UserError, ValidationError
import logging

_logger = logging.getLogger(__name__)

class Task(models.Model):
    _inherit = "project.task"

    support_user_ids = fields.Many2many('res.users', string="Support Contact")
    
    @api.onchange('user_id')
    def _onchange_support_user_ids(self):
        """
        When user_id changes, support_user_ids domain will change to avoid
        selected user_id to appear in many2many field
        """
        if self.user_id:
            domain = [('id', '!=', self.user_id.id)]
            return {'domain': {'support_user_ids': domain}}
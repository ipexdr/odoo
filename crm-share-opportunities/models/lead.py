# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import AccessError, UserError, ValidationError
import logging

_logger = logging.getLogger(__name__)

class Task(models.Model):
    _inherit = "crm.lead"

    shared_users_id = fields.Many2many('res.users', string="Shared Contacts", domain="[('id', '!=', user_id.id)])")
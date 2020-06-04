# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import AccessError, UserError, ValidationError
import logging

_logger = logging.getLogger(__name__)

class Lead(models.Model):
    _inherit = "crm.lead"
    
    # The field wont show the user currently logged in - if the user can already see the opportunity, there's no 
    # need to add himself.
    shared_users_id = fields.Many2many('res.users', string="Shared Contacts", domain="[('id', '!=', uid)]")

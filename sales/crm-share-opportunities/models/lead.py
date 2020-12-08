# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import AccessError, UserError, ValidationError
import logging

_logger = logging.getLogger(__name__)

class Lead(models.Model):
    _inherit = "crm.lead"
    
    # The field will only show salesmen
    shared_users_id = fields.Many2many(
        'res.users', 
        string="Share with Users", 
        domain=lambda self: [("groups_id", "in", self.env.ref("sales_team.group_sale_salesman").id)])

    # TODO: Assigned salesman (user_id) must not appear in field

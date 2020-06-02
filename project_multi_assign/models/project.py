# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import AccessError, UserError, ValidationError
import logging

_logger = logging.getLogger(__name__)

class Task(models.Model):
    _inherit = "project.task"

    support_user_ids = fields.Many2many('res.users', string="Support Contact") 
    # TODO: Default domain shouldnt allow user_id to be selected in support_user_ids    
    
    @api.onchange('user_id')
    def _onchange_support_user_ids(self):
        """
        When user_id changes, support_user_ids domain will change to avoid
        selected user_id to appear in many2many field
        """
        
        if self.user_id:
            domain = [('id', '!=', self.user_id.id)]
            return {'domain': {'support_user_ids': domain}}
        else:
            return {'domain':{'support_user_ids':[]}}
        
    # @api.onchange('support_user_ids')
    # def _subscribe_support_user_ids(self):
    #     """
    #     When 
    #     """
    #     partner_ids = [user.partner_id.id for user in self._origin.support_user_ids]
    #     self._origin.message_subscribe(partner_ids)
        
    def notify_support_users(self):
        """
        Takes the many2many field partner_ids and notifies them about
        the task assignation.
        """
        support_partners = set([user.partner_id.id for user in self.support_user_ids])
        message = f"You have been assigned as a support contact to the task {self.name}."
        _logger.info(support_partners)
        self.message_post(
            subject=f"You have been assigned as support to {self.name}",
            body=message,
            partner_ids = support_partners
        )
    
    def write(self, vals):
        self.notify_support_users()
            
        super(Task, self).write(vals)
        return True
        
    # TODO: Overwrite create() to allow notification when record is created
    
    # TODO: Distinguish if user has been added or not when notifying the assignation,
    # instead of notifying everyone

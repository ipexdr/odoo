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
        
    def notify_support_users(self, users=None):
        """
        Takes the many2many field partner_ids and notifies them about
        the task assignation.
        """

        # If there are no specified users, every user in the support_user_ids
        # field will be notified
        # (This happens only in create() method)
        if users is None:
            support_partners = set([user.partner_id.id for user in self.support_user_ids])
            names = [user.partner_id.name for user in self.support_user_ids] 
        else:
            support_partners = set([user.partner_id.id for user in users])
            names = [user.partner_id.name for user in users] 
            
        # According to the number of members assigned, the message will be different
        if len(support_partners) > 0:
            # Names separated by comma if > 1
            msg_names = ', '.join(names) if len(support_partners) > 1 else names[0]

            if len(support_partners) > 1:
                message = f"{msg_names} have been assigned as a support contact to the task {self.name}."
            else:
                message = f"{msg_names} has been assigned as a support contact to the task {self.name}."
            
            _logger.info(support_partners)
            self.message_post(
                subject=f"You have been assigned as support to {self.name}",
                body=message,
                partner_ids = support_partners
            )
    
    def write(self, vals):
        # Storing old data for comparison
        pre_ids = self.support_user_ids
        
        # Writing database changes
        res = super(Task, self).write(vals)
        
        # Taking new data
        post_ids = self.support_user_ids
    
        # If there is a difference between old and
        # new data, the loop will check if there are
        # new users to be notified
        if pre_ids != post_ids:
            new_users = set()
            
            for user in post_ids:
                if user not in pre_ids:
                    new_users.add(user)
            self.notify_support_users(users=new_users)
            
        return res
        
    @api.model
    def create(self, vals):
        task = super(Task, self).create(vals)
        if vals.get('support_user_ids'):
            task.notify_support_users()
        return task

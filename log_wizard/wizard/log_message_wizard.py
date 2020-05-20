# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class LogMessageWizard(models.TransientModel):
    _name='log.message.wizard'
    _description='Wizard to log a message in chatter'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    message = fields.Html('Contents', default='', sanitize_style=True)

    def action_confirm(self):
        parent = self.env[self._context['parent_model']].browse(self._context['parent_id'])
        msg_subject = self._context['subject']
        
        parent.message_post(
            subject=msg_subject,
            body=self.message,
            partner_ids=[parent.user_id.partner_id.id]
        )
        
        if self._context['to_state']:
            # Change parent state if to_state context
            parent.write({'state':self._context['to_state']})
        
        
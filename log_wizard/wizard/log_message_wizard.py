# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class LogMessageWizard(model.TransistentModel):
    _name='log.message.wizard'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    def _get_partner_id(self):
        return self.env[self._context['parent_model']].browse(self._context['user_id'])

    @api.model
    def _get_default_author(self):
        return self.env.user.partner_id

    partner_id = fields.Many2one('res.partner', string="To:", default=_get_partner_id)
    author_id = fields.Many2one('res.partner', string='Author', default=_get_default_author)
    message = fields.Char(default = f"Hello, {partner_id.name}")

    def action_confirm(self):
        parent = self.env[self._context['parent_model']].browse(self._context['parent_id'])
        msg = self.message
        parent.message_post(body=msg)
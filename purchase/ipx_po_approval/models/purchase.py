# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import AccessError, UserError, ValidationError
import logging

_logger = logging.getLogger(__name__)

class PurchaseOrder(models.Model):
    _inherit = ['purchase.order']


#     can_send_po = fields.Boolean(compute = '_can_send_po')
    user_access_level = fields.Integer(compute='_compute_user_access', default=0)
    is_approve_visible = fields.Boolean(compute='_is_approve_visible', default=False)
    
    pre_approved = fields.Float(store=True, default=False)
    final_approved = fields.Float(store=True, default=False)
    
    
    # Overriding original action_cancel to ask for approval if user is not assistant nor manager
    def button_cancel(self):
        if not self.env.user.has_group('po_approval.group_purchase_assistant') and self.state not in ('draft'):
            # Getting all assistant/manager users
            all_users = self.env['res.users'].search([('active', '=', True)])
            my_users_group = all_users.filtered(lambda user: user.has_group('po_approval.group_purchase_assistant'))

            partner_ids = []
            for user in my_users_group:
                partner_ids.append(user.partner_id.id)
                
            _logger.info(f"Action cancel - po approval assistants {partner_ids}")
            view = self.env.ref('log_wizard.log_message_wizard_view')
            wiz = self.env['log.message.wizard'].create({})      
            wiz_name = "PO cancellation request"
            
            ctx = {
                'subject': wiz_name,
                'partner_ids': partner_ids,
                'parent_model': self._name,
                'parent_id': self.id,
            }
            
            return {
                'name': wiz_name,
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'log.message.wizard',
                'views': [(view.id, 'form')],
                'view_id': view.id,
                'target': 'new',
                'res_id': wiz.id,
                'context': ctx
            }
        else:
            for order in self:
                for inv in order.invoice_ids:
                    if inv and inv.state not in ('cancel', 'draft'):
                        raise UserError("Unable to cancel this purchase order. You must first cancel the related vendor bills.")
            
            view = self.env.ref('log_wizard.log_message_wizard_view')
            wiz = self.env['log.message.wizard'].create({})      
            wiz_name = "RFQ cancellation reason"
            
            ctx = {
                'subject': wiz_name,
                'to_state': 'cancel',
                'parent_model': self._name,
                'parent_id': self.id,
            }
            
            return {
                'name': wiz_name,
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'log.message.wizard',
                'views': [(view.id, 'form')],
                'view_id': view.id,
                'target': 'new',
                'res_id': wiz.id,
                'context': ctx
            }

    @api.depends('user_id')
    def _compute_user_access(self):
        # If user is manager - access level = 2
        # If user is assistant - access level = 1
        # If user is user - access level = 0
        _logger.info("_compute_user_access")
        if self.env.user.has_group('purchase.group_purchase_manager'):
            self.user_access_level = 2
            _logger.info("level 2")
        elif self.env.user.has_group('po_approval.group_purchase_assistant'):
            self.user_access_level = 1
            _logger.info("level 1")
        else:
            self.user_access_level = 0
            _logger.info("level 0")

#     @api.depends('user_access_level')
#     def _can_send_po(self):
#         _logger.info("_can_send_po")
        
#         user_access_level = self.user_access_level
#         env_lock_conf_po = self.company_id.po_lock == 'lock'
        
#         _logger.info(f"user level -> {user_access_level}")
#         _logger.info(f"lock conf PO -> {env_lock_conf_po}")
#         if env_lock_conf_po:
#             if user_access_level > 0 and self.state in ('done', 'purchase'):
#                 self.can_send_po = True
#                 _logger.info(f"can send -> True")
#             else:
#                 self.can_send_po = False
#                 _logger.info(f"can send -> False")
#         else:
#             self.can_send_po = True
#             _logger.info(f"can send -> True")
    
    @api.depends('user_id')
    def _is_approve_visible(self):
        
        if self.env.user.has_group('purchase.group_purchase_manager'):
            is_user_manager = True
            is_user_assistant = False
        else:
            is_user_manager = False
            if self.env.user.has_group('po_approval.group_purchase_assistant'):
                is_user_assistant = True
            else:
                is_user_assistant = False
        
        if self.state in ('to approve'):
            if (is_user_assistant and not self.pre_approved) or (is_user_manager):
                self.is_approve_visible = True
            else:
                self.is_approve_visible = False
        else:
            self.is_approve_visible = False

    # Overriding original method to allow two-people approval
    def button_approve(self, force=False, override=False):
        # all_users = self.env['res.users'].search([('active', '=', True)])
        
        if self.env.user.has_group('purchase.group_purchase_manager') or override:
            self.write({'pre_approved':True, 'final_approved':True})
            self.write({'state': 'purchase', 'date_approve': fields.Datetime.now()})
            self.filtered(lambda p: p.company_id.po_lock == 'lock').write({'state': 'done'})
            return {}
        else:
            self.pre_approved = True
            po_number = self.name

            msg = f"<p>The Purchase Order <b>{po_number}</b> needs final approval.</p>"
            msg += f"<p><b>Vendor</b>: {self.partner_id.name}</p>"
            try:
                msg += f"<p><b>End Customer</b>: {self.end_customer_id.name}</p>"
            except:
                pass

            
            all_users = self.env['res.users'].search([('active', '=', True)])

            my_users_group = all_users.filtered(lambda user: user.has_group('purchase.group_purchase_manager'))
            
            partner_ids = []
            for user in my_users_group:
                partner_ids.append(user.partner_id.id)
                        
            self.message_post(
                subject='Purchase Order pending for Approval',
                body=msg,
                partner_ids=tuple(partner_ids),
            )
            return {}
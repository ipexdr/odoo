# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import AccessError, UserError, ValidationError


class PurchaseOrder(models.Model):
    _inherit = ['purchase.order']

    end_customer_id = fields.Many2one('res.partner', string='End Customer', tracking=True)
    end_contact_id = fields.Many2one('res.partner', string='Contact', tracking=True)
    
    ref_customer_quote_id = fields.Many2one('sale.order', string='Customer Quote ID', tracking=True)
    
    vendor_contact_id = fields.Many2one('res.partner', string='Vendor Contact', tracking=True)

    courier_id = fields.Many2one('res.partner', string='Courier', tracking=True)

    is_vendor_quote = fields.Boolean('Vendor Quote is attached', store=True, default=False)
    is_customer_po = fields.Boolean('Customer PO is attached', store=True, default=False)

#     is_user_assistant = fields.Boolean(compute='_is_user_assistant')
#     is_user_manager = fields.Boolean(compute='_is_user_manager')
    is_approve_visible = fields.Boolean(compute='_is_approve_visible', default=False)
    
    pre_approved = fields.Float(store=True, default=False)
    final_approved = fields.Float(store=True, default=False)
            
    @api.depends('user_id')
    def _is_approve_visible(self):
        
        if self.env.user.has_group('purchase.group_purchase_manager'):
            is_user_manager = True
            is_user_assistant = False
        else:
            is_user_manager = False
            if self.env.user.has_group('po_end_customer.group_purchase_assistant'):
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

    # Overriding original method to verify if required files
    # are uploaded
    def button_confirm(self):
        for order in self:
            if order.is_vendor_quote and order.is_customer_po:
                if order.state not in ['draft', 'sent']:
                    continue
                order._add_supplier_to_product()
                # Deal with double validation process
                if order.company_id.po_double_validation == 'one_step'\
                        or (order.company_id.po_double_validation == 'two_step'\
                            and order.amount_total < self.env.company.currency_id._convert(
                                order.company_id.po_double_validation_amount, order.currency_id, order.company_id, order.date_order or fields.Date.today()))\
                        or order.user_has_groups('purchase.group_purchase_manager'):
                    order.button_approve(override=True)
                else:
                    order.write({'state': 'to approve'})
            else:
                raise UserError("Unable to confirm order. Please check that the required files are attached.")
        return True

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

            order_id = self.id

            domain = self.env['ir.config_parameter'].sudo().get_param('web.base.url')

            url = f"{domain}/web#id={order_id}&action=316&model=purchase.order&view_type=form&cids=1&menu_id=188"

            msg = f"<p>The Purchase Order <b>{po_number}</b> needs final approval.</p>"
            msg += f"<p><b>Vendor</b>: {self.partner_id.name}</p>"
            msg += f"<p><b>End Customer</b>: {self.end_customer_id.name}</p>"
            msg += f"<p>Click <b><a href=\"{url}\">here</a></b> to view the order."

            
            all_users = self.env['res.users'].search([('active', '=', True)])

            my_users_group = all_users.filtered(lambda user: user.has_group('purchase.group_purchase_manager'))
            
            partner_ids = []
            for user in my_users_group:
                partner_ids.append(user.partner_id.id)
            
            self.message_post(body="PO Pre-approved. Waiting for final approval.")
            
#             TODO: change the way the mail is being sent
            self.message_notify(
                subject='Purchase Order pending for Approval',
                body=msg,
                partner_ids=tuple(partner_ids),
                model=self._name,
                res_id=self.id
            )
            return {}

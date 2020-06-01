# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import AccessError, UserError, ValidationError
import logging

_logger = logging.getLogger(__name__)

class PurchaseOrder(models.Model):
    _inherit = ['purchase.order']

    READONLY_STATES = {
        'purchase': [('readonly', True)],
        'done': [('readonly', True)],
        'cancel': [('readonly', True)],
    }

    end_customer_id = fields.Many2one('res.partner', string='End Customer', tracking=True, required=True, states=READONLY_STATES)
    end_contact_id = fields.Many2one('res.partner', string='Contact', tracking=True, states=READONLY_STATES)
    
    ref_customer_quote_id = fields.Many2one('sale.order', string='Customer Quote ID', tracking=True)
    
    # vendor_contact_id = fields.Many2one('res.partner', string='Vendor Contact', tracking=True)

    courier_id = fields.Many2one('res.partner', string='Courier', tracking=True)

    is_vendor_quote = fields.Boolean('Vendor Quote is attached', store=True, default=False)
    is_customer_po = fields.Boolean('Customer PO is attached', store=True, default=False)
    

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
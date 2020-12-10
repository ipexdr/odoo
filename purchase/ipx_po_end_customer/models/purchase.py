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

    # is_vendor_quote = fields.Boolean('Vendor Quote is attached', store=True, default=False)
    # is_customer_po = fields.Boolean('Customer PO is attached', store=True, default=False)
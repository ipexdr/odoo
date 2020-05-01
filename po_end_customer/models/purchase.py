# -*- coding: utf-8 -*-

from odoo import models, fields, api

class PurchaseOrder(models.Model):
    _inherit = ['purchase.order']

    end_customer_id = fields.Many2one('res.partner', string='End Customer', tracking=True)
    end_contact_id = fields.Many2one('res.partner', string='Contact', tracking=True)

    ref_customer_quote_id = fields.Many2one('sale.order', string='Customer Quote ID', tracking=True)
    
    vendor_contact_id = fields.Many2one('res.partner', string='Vendor Contact', tracking=True)

    courier_id = fields.Many2one('res.partner', string='Courier', tracking=True)
# -*- coding: utf-8 -*-

from odoo import models, fields, api

class PurchaseOrder(models.Model):
    _inherit = ['purchase.order']

    customer_id = fields.Many2one('res.partner', string='End Customer', tracking=True)
    courier_id = fields.Many2one('res.partner', string='Courier', tracking=True)
    contact_id = fields.Many2one('res.partner', string='Contact', tracking=True)
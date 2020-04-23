# -*- coding: utf-8 -*-

from odoo import models, fields, api

class PurchaseOrder(models.Model):
    _inherit = ['purchase.order']

    client_id = fields.Many2one('res.partner', string='Final Client', states=READONLY_STATES, tracking=True)
    
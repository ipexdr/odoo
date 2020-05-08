# -*- coding: utf-8 -*-

from odoo import api, fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    po_manager = fields.Many2one('res.users', string="Purchase Orders Manager", help="The user responsible for the final approval of a PO.")

    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        res.update(
            po_manager = self.env['ir.config_parameter'].sudo().get_param('po_end_customer.po_manager')
        )

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param('po_end_customer.po_manager', self.po_manager)

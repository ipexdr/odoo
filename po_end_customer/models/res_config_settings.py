# -*- coding: utf-8 -*-

from odoo import api, fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    
    po_manager = fields.Many2one('res.users', string="Purchase Orders Manager", help="The user responsible for a PO's final approval.", default=False)

#     @api.model
#     def get_values(self):
#         res = super(ResConfigSettings, self).get_values()
#         res.update(
#             po_manager = int(self.env['ir.config_parameter'].sudo().get_param('po_end_customer.po_manager'))
#         )
#         return res

#     def set_values(self):
#         super(ResConfigSettings, self).set_values()
#         self.env['ir.config_parameter'].sudo().set_param('po_end_customer.po_manager', self.po_manager)

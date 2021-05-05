# -*- coding: utf-8 -*-

from odoo import api, fields, models
from ast import literal_eval
import logging

_logger = logging.getLogger(__name__)

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    po_manager = fields.Many2one('res.users', string="Purchase Orders Manager", help="The user responsible for a PO's final approval.")
    
    def set_values(self):
    	res = super(ResConfigSettings, self).set_values()
    	self.env['ir.config_parameter'].sudo().set_param('ipx_po_approval.po_manager', self.po_manager.id)
    	return res
    
    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        with_user = self.env['ir.config_parameter'].sudo()
        po_mgr = with_user.get_param('ipx_po_approval.po_manager')
        # _logger.info(f"literal_eval po_mgr -> {literal_eval(po_mgr)}")
        res.update(
        	po_manager=(literal_eval(po_mgr)) if po_mgr else False)
        return res
        
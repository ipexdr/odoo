from odoo import api, fields, models
from datetime import date
import logging

_logger = logging.getLogger(__name__)

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    sales_order_approval_enabled = fields.Boolean("Sales Order Approval", default=False)

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        
        params = self.env['ir.config_parameter'].sudo()
        sales_order_approval_enabled = params.get_param('ipx_sales_approval.sales_order_approval_enabled', default=False)
        
        res.update(
            sales_order_approval_enabled = sales_order_approval_enabled
        )
        return res

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        param = self.env['ir.config_parameter'].sudo()
        param.set_param('ipx_sales_approval.sales_order_approval_enabled', self.sales_order_approval_enabled)
        
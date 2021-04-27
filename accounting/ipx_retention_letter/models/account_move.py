# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

def fields_view_get(self, view_id=None, view_type='form', toolbar=False,
                    submenu=False):
    res = super().fields_view_get(view_id=view_id, view_type=view_type,
                                  toolbar=toolbar, submenu=submenu)
    if toolbar:
        for action in res['toolbar'].get('action'):
            if action.get('xml_id'):
                if action['xml_id'] == 'ipx_retention_letter_report' and self._context.get(
                        'default_type') == 'entry':
                    res['toolbar']['action'].remove(action)
    return res
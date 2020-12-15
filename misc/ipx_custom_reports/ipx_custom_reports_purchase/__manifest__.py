# -*- coding: utf-8 -*-
{
    'name': "Purchase - Custom QWeb Reports",

    'summary': """
        IPX specific custom reports/templates.""",

    'description': """
        - Adds handwritten signature fields at bottom of purchase order
    """,

    'author': "IP Expert DR",
    'website': "http://www.ipexdr.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Purchase',
    'version': '0.1.0',

    # any module necessary for this one to work correctly

    'depends': ['purchase'],

    # always loaded
    'data': [
        # 'security/security.xml',
        # 'security/ir.model.access.csv',
        # 'wizard/log_message_wizard_view.xml'
        'reports/purchase_reports.xml',
    ],
}

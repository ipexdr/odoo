# -*- coding: utf-8 -*-
{
    'name': "Base - Custom QWeb Reports",

    'summary': """
        IPX specific custom reports/templates.""",

    'description': """
        - QWeb reports custom header and footer for clean layout.
    """,

    'author': "IP Expert DR",
    'website': "http://www.ipexdr.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Base',
    'version': '0.1',

    # any module necessary for this one to work correctly

    'depends': ['web'],

    # always loaded
    'data': [
        # 'security/security.xml',
        # 'security/ir.model.access.csv',
        # 'wizard/log_message_wizard_view.xml'
        'views/report_templates.xml',
    ],
}

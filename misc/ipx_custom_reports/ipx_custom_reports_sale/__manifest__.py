# -*- coding: utf-8 -*-
{
    'name': "Sale - Custom QWeb Reports",

    'summary': """
        IPX specific custom reports/templates.""",

    'description': """
        - Removes part number from Sale Order.
        - Adds SO report w/ part number
    """,

    'author': "IP Expert DR",
    'website': "http://www.ipexdr.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sales',
    'version': '0.0.2',

    # any module necessary for this one to work correctly

    'depends': ['sale_management'],

    # always loaded
    'data': [
        # 'security/security.xml',
        # 'security/ir.model.access.csv',
        # 'wizard/log_message_wizard_view.xml'
        'views/sale_report.xml',
    ],
}

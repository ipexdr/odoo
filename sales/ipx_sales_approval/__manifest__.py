# -*- coding: utf-8 -*-
{
    'name': "Sales Approval Process",

    'summary': """
        Adds an approval process for Sales Orders""",

    'description': """
        Adds an approval process if some fields are out
        of a predefined range.
    """,

    'author': "IP Expert DR",
    'website': "http://www.ipexdr.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sales',
    'version': '0.1',

    # any module necessary for this one to work correctly

    'depends': ['sale_management', 'log_wizard'],

    # always loaded
    'data': [
        'data/ir_module_category_data.xml',
        'security/security.xml',
        # 'security/ir.model.access.csv',
        'views/sale_order.xml',
        'data/mail_data.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

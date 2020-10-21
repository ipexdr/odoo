# -*- coding: utf-8 -*-
{
    'name': "Sale Order Approval process",

    'summary': """
        Allows for Sales Order approval process""",

    'description': """
        Based on Purchase's approval process, adds the capability of
        asking for a manager's approval in case some fields are out 
        of their predefined values.
    """,

    'author': "IP Expert DR",
    'website': "http://www.ipexdr.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sales',
    'version': '1.2',

    # any module necessary for this one to work correctly

    'depends': ['sale_management', 'ipx_quote_fields', 'ipx_log_wizard'],

    # always loaded
    'data': [
        'data/ir_module_category_data.xml',
        'security/security.xml',
        # 'security/ir.model.access.csv',
        'views/sale_order.xml',
        'data/mail_data.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],

    'css': [
        'static/src/css/style.css'
    ]
}

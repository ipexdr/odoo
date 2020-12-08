# -*- coding: utf-8 -*-
{
    'name': "User Signature for Accounting",

    'summary': """
        Showing handwritten signature in invoices.""",

    'description': """
        
    """,

    'author': "IP Expert DR",
    'website': "http://www.ipexdr.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Human Resources',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['user_signature', 'account'],

    # always loaded
    'data': [
        # 'security/security.xml',
        # 'security/ir.model.access.csv',
        'views/invoice_report.xml'
    ],
}

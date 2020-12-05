# -*- coding: utf-8 -*-
{
    'name': "Accounting - Custom QWeb Reports",

    'summary': """
        IPX specific custom reports for Accounting.""",

    'description': """
        
    """,

    'author': "IP Expert DR",
    'website': "http://www.ipexdr.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Accounting',
    'version': '0.2',

    # any module necessary for this one to work correctly

    'depends': ['account'],

    # always loaded
    'data': [
        # 'security/security.xml',
        # 'security/ir.model.access.csv',
        'view/report_invoice.xml'
    ],
    # only loaded in demonstration mode
}

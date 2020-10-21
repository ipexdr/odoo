# -*- coding: utf-8 -*-
{
    'name': "Cents Fraction Format for Check Printing",

    'summary': """
        Shows 0/100 format when showing cents in checks.""",

    'description': """
        
    """,

    'author': "IP Expert DR",
    'website': "http://www.ipexdr.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Accounting',
    'version': '0.7',

    # any module necessary for this one to work correctly

    'depends': ['account_check_printing'],

    # always loaded
    # 'data': [
    #     # 'security/security.xml',
    #     # 'security/ir.model.access.csv',
    #     'wizard/log_message_wizard_view.xml'
    # ]
}

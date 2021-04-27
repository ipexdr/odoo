# -*- coding: utf-8 -*-
{
    'name': "Retention Letter",

    'summary': """
        Adds Retention Letter action when a Retention-type tax is selected in an invoice.""",

    'description': """
        
    """,

    'author': "IP Expert DR",
    'website': "http://www.ipexdr.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Accounting',
    'version': '0.2.0',

    # any module necessary for this one to work correctlyy

    'depends': ['account', 'ncf_generator'],

    # always loaded
    'data': [
        'views/report_retention_letter.xml'
        
    ]
}

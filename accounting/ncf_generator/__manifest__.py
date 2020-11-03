# -*- coding: utf-8 -*-
{
    'name': "NCF Generator",

    'summary': """
        Allows categorization and automatic generation of NCF for invoices.""",

    'description': """
        
    """,

    'author': "IP Expert DR",
    'website': "http://www.ipexdr.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Accounting',
    'version': '0.9.1',

    # any module necessary for this one to work correctlyy

    'depends': ['account'],

    # always loaded
    'data': [
        'data/ncf_sequences.xml',
        'data/account_move_types.xml',
        'security/ir.model.access.csv',
        'views/ncf_sequence_views.xml',
        'views/account_move_views.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],

    'css': [
        'static/src/css/style.css'
    ]
}

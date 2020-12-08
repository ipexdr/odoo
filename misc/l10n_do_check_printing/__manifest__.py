# -*- coding: utf-8 -*-
{
    'name': "DO Check Layout",

    'summary': """ Print DO Checks """,

    'description': """
        This module allows to print Dominican Republic payments on pre-printed check paper.
    """,

    'author': "IP Expert DR",
    'website': "http://www.ipexdr.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Accounting',
    'version': '1.0.2',

    # any module necessary for this one to work correctly

    'depends': ['account_check_printing'],

    # always loaded
    'data': [
        'data/do_check_printing.xml',
        'report/print_check.xml',
        'report/print_check_top.xml',
        # 'report/print_check_middle.xml',
        # 'report/print_check_bottom.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],

    'css': [
        'static/src/css/style.css'
    ]
}

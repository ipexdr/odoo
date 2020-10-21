# -*- coding: utf-8 -*-
{
    'name': "Product Extra fields",

    'summary': """
        Adds extra information to Products""",

    'description': """
        IP Expert module for Products.
    """,

    'author': "IP Expert DR",
    'website': "http://www.ipexdr.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sales',
    'version': '0.2.0',

    # any module necessary for this one to work correctly

    'depends': ['sale_management', 'purchase'],

    # always loaded
    'data': [
        'views/product_form.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],

    'css': [
        'static/src/css/style.css'
    ]
}

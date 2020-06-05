# -*- coding: utf-8 -*-
{
    'name': "IP Expert's PDF Formats",

    'summary': """
        Some additional custom PDF Formats for IP Expert.""",

    'description': """
        
    """,

    'author': "IP Expert DR",
    'website': "http://www.ipexdr.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sales',
    'version': '1.0',

    # any module necessary for this one to work correctlyy

    'depends': ['sales'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'report/sale_report.xml',
        # 'data/project_stages.xml',
#         'security/ir.model.access.csv'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],

    'css': [
        'static/src/css/style.css'
    ]
}

# -*- coding: utf-8 -*-
{
    'name': "SCRUM for Project",

    'summary': """
        Adds some scrum-related features to project.""",

    'description': """
        
    """,

    'author': "IP Expert DR",
    'website': "http://www.ipexdr.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Operations/Project',
    'version': '0.5.3',

    # any module necessary for this one to work correctlyy

    'depends': ['project'],

    # always loaded
    'data': [
        # 'security/security.xml',
        'security/ir.model.access.csv',
        'views/project_views.xml',
        'data/project_stages.xml',
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

# -*- coding: utf-8 -*-
{
    'name': "Share Opportunities to other users",

    'summary': """
        A lead owner can allow read access to their own leads/opportunities.""",

    'description': """
        
    """,

    'author': "IP Expert DR",
    'website': "http://www.ipexdr.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sales/CRM',
    'version': '1.0',

    # any module necessary for this one to work correctlyy

    'depends': ['crm'],

    # always loaded
    'data': [
        # 'security/security.xml',
        # 'security/ir.model.access.csv',
        'views/crm_views.xml',
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

# -*- coding: utf-8 -*-
{
    'name': "Final Client and Courier info in PO",

    'summary': """
        Adds the final client and courier fields to the PO model""",

    'description': """
        IP Expert module that adds relevant info about
        the PO's final client information.
        
        Final clients fields:
        - Name
        - Address (only in PDF)
        - Contact (only in PDF)
        - Phone (only in PDF)
        - Website (only in PDF)
        - Contact Email (only in PDF)

        Courier fields:
        - Name
        - Address (only in PDF)
        - Phone (only in PDF)
    """,

    'author': "IP Expert DR",
    'website': "http://www.ipexdr.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Purchase',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['purchase'],

    # always loaded
    'data': [
        # 'security/security.xml',
        # 'security/ir.model.access.csv',
        'views/templates.xml',
        'views/purchase_views.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],

    'css': [
        'static/src/css/style.css'
    ]
}

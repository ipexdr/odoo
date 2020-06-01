# -*- coding: utf-8 -*-
{
    'name': "End Customer and Courier in PO",

    'summary': """
        Adds the end customer and courier fields to the PO model""",

    'description': """
        IP Expert module that adds relevant info about
        the PO's end client.
        
        End customer fields:
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
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['purchase', 'sale'],

    # always loaded
    'data': [
        'security/security.xml',
        # 'security/ir.model.access.csv',
        'views/purchase_views.xml',
        'views/res_config_settings_views.xml',
        'reports/po_report.xml',
        'reports/rfq_report.xml',
        'data/paperformat_us_landscape.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],

    'css': [
        'static/src/css/style.css'
    ]
}

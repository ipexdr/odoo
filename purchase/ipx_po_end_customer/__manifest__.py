# -*- coding: utf-8 -*-
{
    'name': "End Customer in PO",

    'summary': """
        End customer field in PO""",

    'description': """
        IP Expert module that adds relevant info about
        the PO's end client.
        
        - Name
        - Address (only in Report)
        - Contact (only in Report)
        - Phone (only in Report)
        - Website (only in Report)
        - Contact Email (only in Report)
    """,

    'author': "IP Expert DR",
    'website': "http://www.ipexdr.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Purchase',
    'version': '1.2.0',

    # any module necessary for this one to work correctly
    'depends': ['purchase', 'paperformat_us_landscape', 'sale'],

    # always loaded
    'data': [
        # 'security/security.xml',
        'security/ir.model.access.csv',
        'views/purchase_views.xml',
        'reports/purchase_reports.xml',
    ],
}
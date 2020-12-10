# -*- coding: utf-8 -*-
{
    'name': "Courier in Purchase Orders",

    'summary': """
        Adds courier field to the Purchase Orders""",

    'description': """
        IP Expert module that adds relevant info about
        the Courier.

        - Name
        - Address (only in Report)
        - Phone (only in Report)
    """,

    'author': "IP Expert DR",
    'website': "http://www.ipexdr.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Purchase',
    'version': '0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['purchase', 'paperformat_us_landscape'],

    # always loaded
    'data': [
        'views/purchase_views.xml',
        'reports/po_report.xml',
        'reports/rfq_report.xml',
    ]
}

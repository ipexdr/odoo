# -*- coding: utf-8 -*-
{
    'name': "Stock - Custom QWeb Reports",

    'summary': """
        IPX specific custom reports for Inventory.""",

    'description': """
        -Removes product SKU from delivery slip
    """,

    'author': "IP Expert DR",
    'website': "http://www.ipexdr.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Inventory',
    'version': '0.1',

    # any module necessary for this one to work correctly

    'depends': ['stock'],

    # always loaded
    'data': [
        # 'security/security.xml',
        # 'security/ir.model.access.csv',
        'reports/report_deliveryslilp.xml'
    ],
    # only loaded in demonstration mode
}

# -*- coding: utf-8 -*-
{
    'name': "Product Manufacturer w/ Inventory",

    'summary': """
        Add-on for Inventory module""",

    'description': """
        - Adds Manufacturer column to Delivery Slips
    """,

    'author': "IP Expert DR",
    'website': "http://www.ipexdr.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Inventory',
    'version': '0.0.1',

    # any module necessary for this one to work correctly

    'depends': ['stock', 'ipx_product_manufacturer'],

    # always loaded
    'data': [
        'views/report_deliveryslip.xml',
    ]
}

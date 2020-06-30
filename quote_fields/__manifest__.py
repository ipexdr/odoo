# -*- coding: utf-8 -*-
{
    'name': "Quotation Extra Fields",

    'summary': """
        Adds extra fields to Sales quotations and SO""",

    'description': """
        IP Expert module for Sales, adds the fields:
            - List Price
            - Vendor Discount
            - Discounted
            - FOB Total
            - Tariff (%)
            - Tariff Cost
            - Total Tariff Cost
            - Cost
            - Administration Costs
            - Final Cost
            - Total Final Cost
            - Margin
            - Profit Margin
            - Profit
            - Sell Price
    """,

    'author': "IP Expert DR",
    'website': "http://www.ipexdr.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sales',
    'version': '1.3',

    # any module necessary for this one to work correctly

    'depends': ['sale_management', 'purchase'],

    # always loaded
    'data': [
        'data/ir_module_category_data.xml',
        'security/security.xml',
        # 'security/ir.model.access.csv',
        'views/sale_order.xml',
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

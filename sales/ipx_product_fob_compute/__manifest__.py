# -*- coding: utf-8 -*-
{
    'name': "FOB fields in Pricelist",

    'summary': """
        Computes listprice from fields in product category.""",

    'description': """
        
    """,

    'author': "IP Expert DR",
    'website': "http://www.ipexdr.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sales',
    'version': '0.0.1',

    # any module necessary for this one to work correctly

    'depends': ['product'],

    # always loaded
    'data': [
        # 'views/product_price_views.xml',
        # 'views/sale_order.xml'
        # 'security/ir.model.access.csv',
    ]
}

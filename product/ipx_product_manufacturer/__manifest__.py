# -*- coding: utf-8 -*-
{
    'name': "Product Manufacturer",

    'summary': """
        Handles products' brand/manufacturer""",

    'description': """
        Saves products Manufacturer's names, allowing for further categorization in reports.
    """,

    'author': "IP Expert DR",
    'website': "http://www.ipexdr.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sales',
    'version': '0.1.0',

    # any module necessary for this one to work correctly

    'depends': ['product'],

    # always loaded
    'data': [
        'views/product_form.xml',
    ]
}

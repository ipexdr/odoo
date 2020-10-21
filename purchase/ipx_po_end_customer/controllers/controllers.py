# -*- coding: utf-8 -*-
# from odoo import http


# class QuoteFields(http.Controller):
#     @http.route('/quote_fields/quote_fields/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/quote_fields/quote_fields/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('quote_fields.listing', {
#             'root': '/quote_fields/quote_fields',
#             'objects': http.request.env['quote_fields.quote_fields'].search([]),
#         })

#     @http.route('/quote_fields/quote_fields/objects/<model("quote_fields.quote_fields"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('quote_fields.object', {
#             'object': obj
#         })

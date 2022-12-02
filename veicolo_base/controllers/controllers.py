# -*- coding: utf-8 -*-
# from odoo import http


# class VeicoloBase(http.Controller):
#     @http.route('/veicolo_base/veicolo_base', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/veicolo_base/veicolo_base/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('veicolo_base.listing', {
#             'root': '/veicolo_base/veicolo_base',
#             'objects': http.request.env['veicolo_base.veicolo_base'].search([]),
#         })

#     @http.route('/veicolo_base/veicolo_base/objects/<model("veicolo_base.veicolo_base"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('veicolo_base.object', {
#             'object': obj
#         })

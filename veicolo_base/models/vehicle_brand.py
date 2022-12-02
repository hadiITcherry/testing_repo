# -*- coding: utf-8 -*-

from odoo import api, fields, models


class VehicleBrand(models.Model):
    _name = 'vehicle.brand'
    _description = 'Brand of the vehicle'
    _order = 'name asc'

    name = fields.Char('Brand', required=True)
    image_128 = fields.Image("Logo", max_width=128, max_height=128)
    model_ids = fields.One2many('vehicle.model', 'brand_id')
    vehicle_type = fields.Selection([('car', 'Car'), ('bike', 'Bike')], default='car')

    @api.depends('model_ids')
    def _compute_model_count(self):
        Model = self.env['vehicle.model']
        for record in self:
            record.model_count = Model.search_count([('brand_id', '=', record.id)])

    def action_vehicle_brand(self):
        self.ensure_one()
        view = {
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': 'vehicle.model',
            'name': 'Models',
            'context': {'search_default_brand_id': self.id, 'default_brand_id': self.id}
        }

        return view

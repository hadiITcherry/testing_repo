# -*- coding: utf-8 -*-

from odoo import _, api, fields, models


class VehicleModel(models.Model):
    _name = 'vehicle.model'
    _description = 'Model of a vehicle'
    _order = 'name asc'

    name = fields.Char('Model name', required=True)
    brand_id = fields.Many2one('vehicle.brand', 'Brand', required=True, help='Brand of the vehicle')
    vehicle_type = fields.Selection([('car', 'Car'), ('bike', 'Bike')], default='car')
    image_128 = fields.Image(related='brand_id.image_128', max_width=128, max_height=128)

    def action_vehicle_model(self):
        self.ensure_one()
        view = {
            'type': 'ir.actions.act_window',
            'view_mode': 'kanban,tree,form',
            'res_model': 'purchase.order',
            'name': _('Vehicles'),
            'context': {'search_default_model_id': self.id, 'default_model_id': self.id}
        }

        return view

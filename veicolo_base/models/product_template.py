# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

FUEL_TYPES = [
    ('diesel', 'Diesel'),
    ('gasoline', 'Gasoline'),
    ('hybrid', 'Hybrid'),
    ('electric', 'Electric'),
    ('other', 'Other'),
]
COLORS_TYPES = [
    ('silver', 'Silver'),
    ('beige', 'Beige'),
    ('white', 'White'),
    ('blue', 'Blue'),
    ('bronze', 'Bronze'),
    ('grey', 'Grey'),
    ('yellow', 'Yellow'),
    ('violet', 'Violet'),
    ('black', 'Black'),
    ('gold', 'Gold'),
    ('orange', 'Orange'),
    ('red', 'Red'),
    ('green', 'Green'),
]

TAX_TYPES = [
    ('export_0', 'Export 0%'),
    ('delivery_ict', 'Intra-Community Delivery'),
    ('vat_21', 'VAT 21%'),
    ('margin_regime', 'Sale subject to the special MARGE regime')
]


class ProductTemplate(models.Model):
    _inherit = "product.template"

    detailed_type = fields.Selection(selection_add=[
        ('vehicle', 'Vehicle'),
    ], ondelete={'vehicle': 'set default'})

    brand_id = fields.Many2one('vehicle.model', 'Model', tracking=True, required=True, help='Model of the vehicle')
    model_id = fields.Many2one('vehicle.brand', 'Make', store=True, readonly=False)
    chassis_number = fields.Char('Chassis Number', help='Unique number written on the vehicle motor (VIN/SN number)',
                                 copy=False)
    construction_year = fields.Integer('First Registration', store=True, readonly=False)
    fuel_type = fields.Selection(FUEL_TYPES, 'Fuel Type', help='Fuel Used by the vehicle', store=True, readonly=False)
    cylinder_capacity = fields.Integer('Cylinder', help='Power in CC of the vehicle', store=True, readonly=False)
    engine_power = fields.Integer('Engine Power', help='Power in kW of the vehicle', store=True, readonly=False)
    color = fields.Selection(COLORS_TYPES, 'Color', help='Color of  the vehicle', store=True, readonly=False)
    plate_number = fields.Char(string='Plate Number', required=False)
    number_of_km = fields.Float(string='Mileage', help='Odometer measure of the vehicle at the moment of this log')

    #  not required fields
    license_plate = fields.Char(tracking=True, help='License plate number of the vehicle (i = plate number for a car)')
    horsepower = fields.Integer(readonly=False)
    horsepower_tax = fields.Float('Horsepower Taxation', readonly=False)
    co2 = fields.Float('CO2 Emissions', help='CO2 emissions of the vehicle', readonly=False)
    co2_standard = fields.Char(readonly=False)
    # image_128 = fields.Image(related='model_id.image_128', readonly=True)
    transmission = fields.Selection([('manual', 'Manual'), ('automatic', 'Automatic')], 'Transmission',
                                    help='Transmission Used by the vehicle',
                                    readonly=False)

    seats = fields.Integer('Seatss Number', help='Number of seats of the vehicle', readonly=False)

    # fields related to price

    price_with_ttc = fields.Boolean(default=False)
    net_price = fields.Monetary(currency_field='currency_id', string='Net Price',
                                help='Price of the vehicle with VAT not included', compute='_calc_price_checkbox',
                                store=True)
    vat_type = fields.Selection(TAX_TYPES, 'VAT Type', computed='_calc_price_checkbox')
    vat_amount = fields.Monetary(currency_field='currency_id', string='VAT amount',
                                 help='Tax amount computed depending on the net price',
                                 readonly=True, computed='_calc_price_checkbox', store=True)
    total_price = fields.Monetary(currency_field='currency_id', string='Price',
                                  help='Price of the vehicle including VAT', compute='_calc_price_checkbox',
                                  store=True)

    # Documents Fields Purchases:
    registration_licensing = fields.Binary(string='Vehicle Registrations & Licensing Document', required=True)
    technical_control = fields.Binary(string='Technical check/control of the vehicle', required=False)
    purchase_invoice = fields.Binary(string='Purchase Invoice', required=True)
    private_paper = fields.Binary(string='Paper from the private Owner', required=True)
    car_pass = fields.Binary(string='Car Pass', required=False)
    conformity_certificate = fields.Binary(string='Certificate of Conformity', required=True)

    # Images of the car (Front side – Left side – Right side – Back side – Interior front – Interior back - …)
    front_side = fields.Image(string='Front side', max_width=100, max_height=100)
    left_side = fields.Image(string='Left side', max_width=100, max_height=100)
    right_side = fields.Image(string='Front side', max_width=100, max_height=100)
    back_side = fields.Image(string='Back side', max_width=100, max_height=100)
    interior_front = fields.Image(string='Interior Front', max_width=100, max_height=100)
    interior_back = fields.Image(string='Interior Back ', max_width=100, max_height=100)
    interior_right = fields.Image(string='Interior Right', max_width=100, max_height=100)
    interior_left = fields.Image(string='Interior Left ', max_width=100, max_height=100)

    # Documents Fields Sales:
    ex_1 = fields.Binary(string='EX1', required=True)
    doc_invoice = fields.Binary(string='Invoice', required=True)
    warranty_export = fields.Binary(string='Exportation Warranty', required=False)
    id_docs = fields.Binary(string='Copy of ID (Recto-Verso) or Passport of the client', required=False)
    warranty_docs = fields.Binary(string='Warranty document', required=False)

    _sql_constraints = [
        ('unique_chassis_number', 'unique(chassis_number)', 'The Chassis number already exits')
    ]

    def _detailed_type_mapping(self):
        type_mapping = super()._detailed_type_mapping()
        type_mapping['vehicle'] = 'service'
        return type_mapping

    # set domain for model to filter the selected models according to the brand value
    @api.onchange('brand_id')
    def set_domain_for_models(self):
        class_obj = self.env['vehicle.model'].search([('brand_id', '=', self.brand_id.id)])
        model_list = []
        for data in class_obj:
            model_list.append(data.id)
        res = {}
        res['domain'] = {'model_id': [('id', 'in', model_list)]}
        if len(model_list) > 0:
            self.model_id = model_list[0]
        else:
            self.model_id = ''
        return res

    # Function calculate net price and total price depends on checkbox
    @api.depends('net_price', 'vat_amount', 'total_price', 'price_with_ttc')
    def _calc_price_checkbox(self):
        if not self.price_with_ttc:
            for r in self:
                if r.vat_type == 'export_0':
                    r.vat_amount = 0
                if r.vat_type == 'delivery_ict':
                    r.vat_amount = 0
                if r.vat_type == 'margin_regime':
                    r.vat_amount = 0
                    r.total_price = r.net_price
                if r.vat_type == 'vat_21':
                    r.vat_amount = r.net_price * 0.21
                r.total_price = r.net_price + r.vat_amount

        else:
            for rec in self:
                if rec.vat_type == 'export_0':
                    rec.vat_amount = 0
                if rec.vat_type == 'delivery_ict':
                    rec.vat_amount = 0
                if rec.vat_type == 'margin_regime':
                    rec.vat_amount = 0
                    rec.total_price = rec.net_price
                if rec.vat_type == 'vat_21':
                    rec.net_price = rec.total_price / 1.21
                    rec.vat_amount = rec.net_price * 0.21





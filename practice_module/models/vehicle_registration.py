from odoo import fields, models, api, _


class vehicle_registration(models.Model):
    _name = 'vehicle.registration'

    name = fields.Char(string="Vehicle No", copy=False, required=True, default=lambda self: _('New'))
    date_of_vehicle_register = fields.Date(string="Vehicle Register Date")
    owner_id = fields.Many2one('res.partner', string="Customer", required=True)
    street = fields.Char(related='owner_id.street', string="Street", store=True)
    street2 = fields.Char(related='owner_id.street2', string="Street2", store=True)
    city = fields.Char(related='owner_id.city', string="City", store=True)
    state_id = fields.Many2one('res.country.state', related='owner_id.state_id', store=True)
    zip = fields.Char(related='owner_id.zip', string="Zip", store=True)
    country_id = fields.Many2one('res.country', related='owner_id.country_id', store=True)
    mobile = fields.Char(string="Mobile No.")
    date_of_birth = fields.Date(string="Date of Birth")
    age = fields.Integer(string="Age")
    image = fields.Binary(string="Image")
    vehicle_type = fields.Selection([('Four Seater', 'Four Seater'),
                                     ('MiniBus', 'MiniBus'),
                                     ('Seven Seater', 'Seven Seater')], string="Vehicle Type", default='Seven Seater')
    price_per_km = fields.Float(string="Price Per KM")
    is_book = fields.Boolean(string="Is Book", copy=False)

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vehicle_code = self.env['ir.sequence'].next_by_code('vehicle.code')
            vals.update({'name':vehicle_code})
        vehicle_id = super(vehicle_registration, self).create(vals)
        return vehicle_id

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        args = args or []
        recs = self.browse()
        if name:
            recs = self.search([('vehicle_type', '=', name)] + args, limit=limit)
        if not recs:
            recs = self.search([('name', operator, name)] + args, limit=limit)
        return recs.name_get()

    @api.multi
    def name_get(self):
#         TYPES = {
#             '4': _('Four Seater'),
#             'mini_bus': _('MiniBus'),
#             '7': _('Seven Seater'),
#         }
        result = []
        for vehicle in self:
            result.append((vehicle.id, "%s / %s / %s" % (vehicle.name, vehicle.vehicle_type, vehicle.price_per_km)))
        return result

from odoo import fields, models, api, _
from odoo.exceptions import UserError

class package_book(models.Model):
    _name = 'package.book'

    @api.multi
    def unlink(self):
        for each in self:
            if each.state not in ('draft', 'cancel'):
                raise UserError(_('You can not delete a Tour Package! Try to cancel it before.'))
        return super(package_book, self).unlink()

    @api.multi
    @api.depends('package_lines.subtotal', 'package_lines.total_km')
    def _compute_total_amount(self):
        self.total_amount = sum([x.subtotal for x in self.package_lines])

    @api.onchange('pickup_address')
    def onchange_pickup_address(self):
        if self.pickup_address and self.partner_id:
            self.street = self.partner_id.street or False
            self.street2 = self.partner_id.street2 or False
            self.city = self.partner_id.city or False
            self.zip = self.partner_id.zip or False
            self.state_id = self.partner_id.state_id.id or False
            self.country_id = self.partner_id.country_id.id or False

    name = fields.Char(strin="Package No", default=lambda self: _('New'), copy=False)
    partner_id = fields.Many2one('res.partner', string="Customer", required=True)
    pickup_address = fields.Boolean(string="Customer Address as Pickup Address")
    street = fields.Char(string="Street")
    street2 = fields.Char(string="Street2")
    city = fields.Char(string="City")
    zip = fields.Char(string="Zip")
    state_id = fields.Many2one('res.country.state', string="State")
    country_id = fields.Many2one('res.country', string="Country")
    driver_id = fields.Many2one('res.partner', string="Driver", required=True)
    mobile = fields.Char(string="Customer Mobile No", related='partner_id.mobile')
    driver_mobile_no = fields.Char(string="Driver Mobile No", related='driver_id.mobile')
    book_date = fields.Date(string="Booking Date", required=True)
    total_amount = fields.Float(compute="_compute_total_amount", string="Total Amount", copy=False, store=True)
    package_lines = fields.One2many('package.booking.line', 'package_id', string="Vehicle Details")
    state = fields.Selection([('draft', 'Draft'),
                              ('confirm', 'Confirmed'),
                              ('cancel', 'Cancel')], string="Status", default='draft')
    invoice_id = fields.Many2one('account.invoice', copy=False, readonly=True,string="Invoice Ref")

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            package_code = self.env['ir.sequence'].next_by_code('package.code')
            vals.update({'name':package_code})
        package_id = super(package_book, self).create(vals)
        return package_id

    @api.multi
    def confirm_booking(self):
        for each in self:
            for line in each.package_lines:
                line.write({'state':'confirm'})
                line.vehicle_id.write({'is_book':True})
            each.write({'state':'confirm'})
        return True

    @api.multi
    def cancel_package(self):
        for each in self:
            for line in each.package_lines:
                if line.filtered(lambda x: x.state in ('running', 'confirm')):
                    raise UserError(_('You can not Cancel a Package.Stop or Cancel the Ride and try to cancel the Package'))
                else:
                    each.write({'state':'cancel'})
        return True

class package_booking_line(models.Model):
    _name = 'package.booking.line'

    @api.depends('total_km', 'vehicle_price')
    def _compute_amount(self):
        for line in self:
            line.update({'subtotal':line.vehicle_price * line.total_km})

    @api.multi
    def cancel_ride(self):
        for each in self:
            each.write({'state':'cancel'})

    package_id = fields.Many2one('package.book', string="Package Reference.")
    vehicle_id = fields.Many2one('vehicle.registration', string="Vehicle", required=True)
    vehicle_price = fields.Float(string="Price Per KM", required=True)
    name = fields.Char(string="Vehicle Information", required=True)
    start_ride_date = fields.Datetime(string="Start Date")
    end_ride_date = fields.Datetime(string="End Date")
    start_km = fields.Integer(string="Start KM")
    end_km = fields.Integer(string="End KM")
    total_km = fields.Integer(string="Total KM")
    subtotal = fields.Float(compute='_compute_amount', string="Subtotal", store=True)
    state = fields.Selection([('draft', 'Draft'),
                              ('confirm', 'Confirmed'),
                              ('running', 'Running'),
                              ('stop', 'Stop'),
                              ('cancel', 'Cancel')], string="Status", copy=False, store=True, default='draft')

    @api.onchange('vehicle_id')
    def onchange_vehicle_id(self):
        if not self.vehicle_id:
            return
        name = self.vehicle_id.name_get()[0][1]
        self.name = name 
        self.vehicle_price = self.vehicle_id.price_per_km
        
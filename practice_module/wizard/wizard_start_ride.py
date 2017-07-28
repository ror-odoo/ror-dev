from odoo import fields, models, api, _
from datetime import datetime

class wizard_start_ride(models.TransientModel):
    _name = 'wizard.start_ride'

    start_ride_date = fields.Datetime(string="Start Ride Date Time", required=1, default=datetime.now())
    start_km = fields.Integer(string="Enter Starting KM", required=1)

    @api.multi
    def start_ride(self):
        print "\n----------context ",self._context
        package_line_id = self.env['package.booking.line'].search([('vehicle_id','=',self._context.get('vehicle_id')),
                                                                   ('package_id','=',self._context.get('package_id'))])
        if package_line_id:
            package_line_id.write({'start_ride_date':self.start_ride_date,
                                   'start_km':self.start_km,
                                   'state':'running'})
        return True
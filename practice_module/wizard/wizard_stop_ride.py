from odoo import fields, models, api, _
from datetime import datetime
from odoo.exceptions import ValidationError
            
class wizard_stop_ride(models.TransientModel):
    _name = 'wizard.stop_ride'

    end_ride_date = fields.Datetime(string="End Ride Date Time", required=1, default=datetime.now())
    end_km = fields.Integer(string="Enter Ending KM", required=1)

    @api.multi
    def end_ride(self):
        package_line_id = self.env['package.booking.line'].search([('vehicle_id', '=', self._context.get('vehicle_id')),
                                                                   ('package_id', '=', self._context.get('package_id'))])

        if package_line_id:
            if self.end_ride_date < package_line_id.start_ride_date:
                raise ValidationError(_('Stop Ride Date Should be greater than Start Ride Date'))
            if self.end_km < package_line_id.start_km:
                raise ValidationError(_('End KM is Should be grater than Start KM'))
            total_km = self.end_km - package_line_id.start_km
            package_line_id.write({'end_ride_date':self.end_ride_date,
                                   'end_km':self.end_km,
                                   'total_km':total_km,
                                   'state':'stop'})
            package_line_id.vehicle_id.write({'is_book':False})
            package_line_id.package_id.write({'state':'invoice'})
        return {'type': 'ir.actions.client', 'tag': 'reload'}

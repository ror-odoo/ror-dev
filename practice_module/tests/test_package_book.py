from odoo.exceptions import UserError, AccessError

from test_common import TestVehicle

class TestPackageBook(TestVehicle):
    def test_package_book(self):
        #create package
        package_id = self.env['package.book'].create({'book_date':'2017-08-01',
                                                      'partner_id':self.partner.id,
                                                      'mobile':self.partner.mobile,
                                                      'driver_id':self.driver.id,
                                                      'driver_mobile_no':self.driver.mobile,
                                                      'street':self.partner.street,
                                                      'city':self.partner.city,
                                                      'state_id':self.partner.state_id.id,
                                                      'zip':self.partner.zip,
                                                      'country_id':self.partner.country_id.id,
                                                      'package_lines':[(0, 0, {'name': self.vehicles.name, 'vehicle_id': self.vehicles.id, 'vehicle_price': 18, 'state':'draft'})]})
        print "\n-----------package_id ", package_id
# 
        # confirm package
        package_id.confirm_booking()
        self.assertTrue(package_id.state == 'confirm','Confirm: something is missing')


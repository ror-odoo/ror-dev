

from odoo.addons.account.tests.account_test_classes import AccountingTestCase


class TestVehicle(AccountingTestCase):
    def setUp(self):
        super(TestVehicle, self).setUp()
        
        self.partner = self.env.ref('base.res_partner_1')
        self.state = self.env.ref('base.state_us_39')
        self.country = self.env.ref('base.us')
        self.driver = self.env['res.partner'].create({'name':'Test Driver',
                                                      'is_driver':True,
                                                      'mobile':+918565488566,
                                                      'email':'test@odoo.com',
                                                      'license_no':'GJ24PFT6512',
                                                      'city':'Scranton',
                                                      'state_id':self.state.id,
                                                      'country_id':self.country.id})
        self.vehicles = self.env['vehicle.registration'].create({'city': u'Gandhinagar',
                                                              'date_of_vehicle_register': '2017-08-01',
                                                               'mobile': '958452136',
                                                               'country_id': self.country.id,
                                                               'price_per_km': 18,
                                                               'state_id': self.state.id,
                                                               'vehicle_type': 'Seven Seater',
                                                               'owner_id': self.partner.id})

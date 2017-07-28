
# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'Transport Service ',
    'version' : '1.1',
    'summary': 'Transport Service',
    'sequence': 30,
    'description': """Transport Service""",
    'category': 'sale',
    'depends' : ['base_setup', 'sale'],
    'data': 
        [
            'security/ir.model.access.csv',
            'data//ir_sequence.xml',
            'wizard/wizard_start_ride_view.xml',
            'wizard/wizard_stop_ride_view.xml',
            'wizard/wizard_create_invoice_view.xml',
            'views/vehicle_registration_view.xml',
            'views/res_partner_view.xml',
            'views/package_book_view..xml',
        ],
    'installable': True,
    'application': False,
    'auto_install': False
}

# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import json
import logging
from werkzeug.exceptions import Forbidden
from odoo import http, tools, _
from odoo.http import request
# from odoo.addons.base.ir.ir_qweb.fields import nl2br
# from odoo.addons.website.models.website import slug
# from odoo.addons.website.controllers.main import QueryURL
# from odoo.exceptions import ValidationError
# from odoo.addons.website_form.controllers.main import WebsiteForm
# 
# _logger = logging.getLogger(__name__)
# 
# PPG = 20  # Products Per Page
# PPR = 4   # Products Per Row

class WebsiteVehicle(http.Controller):
    
    @http.route(['/vehicles',
                 '/vehicles/country/<int:country_id>',
                 '/vehicles/country/<country_name>-<int:country_id>', ], type='http', auth="public", website=True)
    def vehicles(self, country_id=0, country_name='', **post):
        domain = []
        vehicle_name = post.get('search','')
        Vehicles = request.env['vehicle.registration']
        Country = request.env['res.country']
        countries = Vehicles.sudo().read_group(domain, ['id', 'country_id'], groupby="country_id", orderby="country_id")
        country_count = Vehicles.sudo().search_count(domain)
        if country_id:
            domain += [('country_id', '=', country_id)]
            curr_country = Country.browse(country_id)
            if country_id not in (x['country_id'][0] for x in countries if x['country_id']):
                if curr_country.exists():
                    countries.append({
                        'country_id_count': 0,
                        'country_id': (curr_country.id, curr_country.name)
                    })
                countries.sort(key=lambda d: d['country_id'] and d['country_id'][1])
        if vehicle_name:
            domain += [('name','ilike',post.get('search'))]
        countries.insert(0, {
            'country_id_count': country_count,
            'country_id': (0, _("All Countries"))
        })
        vehicle_ids = Vehicles.search(domain)
        vals = {'vehicles':vehicle_ids,
                'countries': countries,
                'current_country_id': country_id or 0,
                'current_country': curr_country if country_id else False, }
        
        return request.render("practice_module.vehicles", vals)

    @http.route(['/vehicles/<model("vehicle.registration"):vehicle>'], type='http', auth="public", website=True)
    def vehicles_detail(self, vehicle, **post):
        values = {}
        values['main_object'] = values['vehicle'] = vehicle
        return request.render("practice_module.details", values)

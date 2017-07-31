from odoo import fields, models, api


class res_partner(models.Model):
    _inherit = 'res.partner'

    is_driver = fields.Boolean(string="Driver")
    license_no = fields.Char(string="License No")

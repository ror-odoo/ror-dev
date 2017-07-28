from odoo import fields, models, api, _

class wizard_create_invoice(models.TransientModel):
    _name = 'wizard.create_invoice'

    invoice_date = fields.Date(string="Invoice Date", required=True)


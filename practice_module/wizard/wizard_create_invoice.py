from odoo import fields, models, api, _
from odoo.exceptions import Warning

class wizard_create_invoice(models.TransientModel):
    _name = 'wizard.create_invoice'

    invoice_date = fields.Date(string="Invoice Date", required=True)

    @api.multi
    def create_invoice(self):
        acc_obj = self.env['account.invoice']
        package_id = self.env['package.book'].browse(self._context.get('active_id'))
#         if all([line.state == 'cancel' for line in package_id.package_line]):
#             raise Warning('You Can not unable to create invoice because all ride has been canceled ')
        invoice_id = acc_obj.search([('partner_id', '=', package_id.partner_id.id),
                                     ('state', '=', 'draft'),
                                     ('package_id', '=', package_id.id)], limit=1)
        journal_id = acc_obj._default_journal()
        invoice_line_account_id = self.env['account.invoice.line'].with_context({'journal_id':journal_id.id})._default_account()
        if not invoice_id:
            invoice_id = self.env['account.invoice'].create({'partner_id':package_id.partner_id.id,
                                                             'journal_id':journal_id.id,
                                                             'account_id':package_id.partner_id.property_account_receivable_id.id,
                                                             'date_invoice':self.invoice_date,
                                                             'package_id':package_id.id,
                                                             'origin':package_id.name})
        for line in package_id.package_lines:
            if not line.invoiced and line.state == 'stop':
                line_vals = {'name':line.name,
                         'account_id':invoice_line_account_id,
                         'quantity':line.total_km,
                         'price_unit':line.vehicle_price,
                         'invoice_id':invoice_id.id}
                invoice_id.write({'invoice_line_ids':[(0, 0, line_vals)]})
                line.write({'invoiced':True})
        return True

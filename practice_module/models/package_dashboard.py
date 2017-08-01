from odoo import fields, models, api, _
from datetime import datetime, date
from odoo import tools

class package_dashboard(models.Model):
    _name = 'package.dashboard'
    _auto = False

    book_date = fields.Date(string="Package Date")
    total_amount = fields.Float(string="Total Amount")
#     state = fields.Selection([('draft', 'Draft'),
#                               ('confirm', 'Confirmed'),
#                               ('cancel', 'Cancel')], string="Status", default='draft')
#     start_ride = fields.Datetime()
#     end_ride = fields.Datetime()

    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        to_day = datetime.strftime(date.today(), '%Y-%m-%d')
        sql = """CREATE OR REPLACE VIEW package_dashboard AS (
                 SELECT
                    id as id,
                    book_date as book_date,
                    sum(total_amount) as total_amount
                FROM
                    package_book
                GROUP By id,book_date)"""
        self._cr.execute(sql)

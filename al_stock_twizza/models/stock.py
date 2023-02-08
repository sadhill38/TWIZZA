from odoo import fields, models
from dateutil.relativedelta import relativedelta


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    date_dl = fields.Date(string="Date (DLC/DLUO)")

    def write(self, vals):
        if self.product_id and vals.get('date_dl'):
            date_dl = fields.Date.from_string(vals['date_dl'])
            existing_lot = self.env['stock.production.lot'].search([
                ('product_id', '=', self.product_id.id),
                ('name', '=', date_dl.strftime("%d%m%Y")),
            ], limit=1)
            if existing_lot:
                vals.update({
                    'lot_id': existing_lot.id
                })
            else:
                dluo = date_dl if self.product_id.duration_type == 'dluo' else False
                dlc = date_dl if self.product_id.duration_type == 'dlc' else False
                rm_date = date_dl - relativedelta(days=self.product_id.removal_time)
                alert_date = date_dl - relativedelta(days=self.product_id.alert_time)

                new_lot = self.env['stock.production.lot'].create({
                    'name': date_dl.strftime("%d%m%Y"),
                    'product_id': self.product_id.id,
                    'life_date': dlc,
                    'use_date': dluo,
                    'removal_date': rm_date,
                    'alert_date': alert_date,
                    'company_id': self.env.company.id,
                })
                vals.update({
                    'lot_id': new_lot.id,
                })
        return super().write(vals)

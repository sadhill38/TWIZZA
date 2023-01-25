from odoo import fields, models


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    date_dl = fields.Date(string="Date (DLC/DLUO)")

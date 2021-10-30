from odoo import fields, models


class ProductPriceListInherit(models.Model):
    _inherit = "product.pricelist"

    company_id = fields.Many2one(default=lambda x: x.env.company.id)

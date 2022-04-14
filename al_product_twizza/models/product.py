from odoo import fields, models


class ProductProduct(models.Model):
    _inherit = 'product.product'

    unit_volume = fields.Float('Unit Volume', digits='Volume')

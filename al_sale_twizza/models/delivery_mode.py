from odoo import fields, models, api


class DeliveryMode(models.Model):
    _name = 'delivery.mode'
    _description = 'Delivery Mode'

    name = fields.Char(string="Name", required=True)

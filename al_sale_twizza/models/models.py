from odoo import fields, models, api


class DeliveryMode(models.Model):
    _name = 'delivery.mode'
    _description = 'Delivery Mode'

    name = fields.Char(string="Name", required=True)


class PaymentMode(models.Model):
    _name = 'payment.mode'
    _description = 'Payment Mode'

    name = fields.Char(string="Name", required=True)


class CustomerType(models.Model):
    _name = 'res.partner.type'
    _description = 'Partner Type'

    name = fields.Char(string="Name", required=True)

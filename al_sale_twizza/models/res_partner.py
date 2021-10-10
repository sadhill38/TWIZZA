from odoo import fields, models, api


class ResPartnerInherit(models.Model):
    _inherit = "res.partner"

    delivery_mode_id = fields.Many2one("delivery.mode", string="Delivery Mode")
    payment_mode_id = fields.Many2one("payment.mode", string="Payment Mode")
    partner_type_id = fields.Many2one("res.partner.type", string="Partner Type")
    # Boolean
    home_consumption = fields.Boolean(string="Home Consumption")
    out_home_consumption = fields.Boolean(string="Out-Of-Home Consumption")

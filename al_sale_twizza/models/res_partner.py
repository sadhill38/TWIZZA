from odoo import fields, models, api


class ResPartnerInherit(models.Model):
    _inherit = "res.partner"

    delivery_mode_id = fields.Many2one("delivery.mode", string="Delivery Mode")

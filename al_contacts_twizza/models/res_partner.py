from odoo import fields, models, api


class ResPartnerInherit(models.Model):
    _inherit = "res.partner"

    company_id = fields.Many2one(default=lambda x: x.env.company.id)

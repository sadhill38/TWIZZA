from odoo import fields, models, api


class AccountPaymentTerm(models.Model):
    _inherit = "account.payment.term"

    user_ids = fields.Many2many('res.users', string="Users")


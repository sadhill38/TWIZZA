from odoo import models


class ResPartnerInherit(models.Model):
    _inherit = "res.partner"

    def action_view_partner_invoices(self):
        action = super(ResPartnerInherit, self).action_view_partner_invoices()
        action['context'].update({
            'create': False,
        })
        return action

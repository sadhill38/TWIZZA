from odoo import models


class ResPartnerInherit(models.Model):
    _inherit = "res.partner"

    def action_view_partner_invoices(self):
        action = super(ResPartnerInherit, self).action_view_partner_invoices()
        cannot_create_or_edit = (
            self.env.user.has_group('al_account_twizza.group_account_invoice_commercial') and not
            self.env.user.has_group('al_account_twizza.group_account_invoice_adv')
        )
        if cannot_create_or_edit:
            action['context'].update({
                'create': False,
                'edit': False
            })
        return action

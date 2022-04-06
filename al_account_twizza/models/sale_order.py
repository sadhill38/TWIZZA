from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_view_invoice(self):
        action = super(SaleOrder, self).action_view_invoice()
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

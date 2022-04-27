from odoo import models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    def action_view_invoice(self):
        action = super(PurchaseOrder, self).action_view_invoice()
        if not self.env.user.has_group('account.group_account_manager'):
            action['context'].update({
                'create': False,
                'edit': False
            })
        return action

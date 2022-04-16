from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_view_invoice(self):
        action = super(SaleOrder, self).action_view_invoice()
        if not self.env.user.has_group('account.group_account_manager'):
            action['context'].update({
                'create': False,
                'edit': False
            })
        return action

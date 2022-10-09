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


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    def _prepare_account_move_line(self, move):
        res = super()._prepare_account_move_line(move)
        res.update({
            'intrastat_transaction_id': self.order_id.partner_id.default_intrastat_id[:1].id,
        })
        return res

from odoo import models, api, exceptions, _


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

    @api.constrains('partner_id')
    def _check_if_partner_is_locked(self):
        for rec in self:
            if rec.partner_id.lock_on_sales:
                # raise exceptions.UserError(_(
                #     "The partner %s is locked because of invoicing issues, "
                #     "if it's an urgent mater please contact your administrator"
                # ) % rec.partner_id.name)
                raise exceptions.UserError(_(
                    "Taking orders for the customer %s is locked, because of late payment, "
                    "please regularize the situation and inform your accounting department."
                ) % rec.partner_id.name)

    def action_confirm(self):
        self._check_if_partner_is_locked()
        return super(SaleOrder, self).action_confirm()

    def action_quotation_send(self):
        self._check_if_partner_is_locked()
        return super(SaleOrder, self).action_quotation_send()



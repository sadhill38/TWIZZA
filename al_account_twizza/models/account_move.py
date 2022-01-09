from odoo import models
import logging

_logger = logging.getLogger(__name__)


class AccountMoveInherit(models.Model):
    _inherit = "account.move"

    def post(self):
        # bypass access right check on action_post if group_create_invoices_from_sales
        if self.env.user.has_group('al_account_twizza.group_account_invoice_adv'):
            self = self.sudo()
        return super(AccountMoveInherit, self).post()



# class AccountMoveReversalInherit(models.TransientModel):
#     _inherit = "account.move.reversal"
#
#     def reverse_moves(self):
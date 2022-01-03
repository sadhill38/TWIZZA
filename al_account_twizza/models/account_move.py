from odoo import models
import logging

_logger = logging.getLogger(__name__)


class AccountMoveInherit(models.Model):
    _inherit = "account.move"

    def action_post(self):
        # bypass access right check on action_post if group_create_invoices_from_sales
        if self.env.user.has_group('al_account_twizza.group_account_reports_reader'):
            self = self.sudo()
        return super(AccountMoveInherit, self).action_post()

from odoo import models, api, fields
import logging

_logger = logging.getLogger(__name__)


class AccountMoveInherit(models.Model):
    _inherit = "account.move"

    payment_mode_id = fields.Many2one("payment.mode", string="Payment Mode", related="partner_id.payment_mode_id")

    def post(self):
        # bypass access right check on action_post if group_create_invoices_from_sales
        if self.env.user.has_group('al_account_twizza.group_account_invoice_adv'):
            self = self.sudo()
        return super(AccountMoveInherit, self).post()

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        super()._onchange_partner_id()
        if self.partner_id.default_intrastat_transport_id:
            self.intrastat_transport_mode_id = self.partner_id.default_intrastat_transport_id.id

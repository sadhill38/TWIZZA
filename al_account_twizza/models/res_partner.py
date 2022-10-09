from odoo import models, fields


class ResPartnerInherit(models.Model):
    _inherit = "res.partner"

    default_intrastat_id = fields.Many2one("account.intrastat.code", string="Default intrastat code")

    def action_view_partner_invoices(self):
        action = super(ResPartnerInherit, self).action_view_partner_invoices()
        if not self.env.user.has_group('account.group_account_manager'):
            action['context'].update({
                'create': False,
                'edit': False
            })
        return action

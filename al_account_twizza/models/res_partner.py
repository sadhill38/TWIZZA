from odoo import models, fields


class ResPartnerInherit(models.Model):
    _inherit = "res.partner"

    default_intrastat_id = fields.Many2one(
        comodel_name="account.intrastat.code",
        string="Default intrastat code",
        domain=[('type', '=', 'transaction')]
    )
    default_intrastat_transport_id = fields.Many2one(
        comodel_name="account.intrastat.code",
        string="Default intrastat Transport mode",
        domain=[('type', '=', 'transport')]
    )
    default_incoterm_id = fields.Many2one('account.incoterms', string='Incoterm')

    def action_view_partner_invoices(self):
        action = super(ResPartnerInherit, self).action_view_partner_invoices()
        if not self.env.user.has_group('account.group_account_manager'):
            action['context'].update({
                'create': False,
                'edit': False
            })
        return action

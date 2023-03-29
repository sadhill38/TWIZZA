from odoo import fields, models, api
import json
from lxml import etree


class ResPartnerInherit(models.Model):
    _inherit = "res.partner"

    delivery_mode_id = fields.Many2one("delivery.mode", string="Delivery Mode")
    payment_mode_id = fields.Many2one("payment.mode", string="Payment Mode")
    partner_type_id = fields.Many2one("res.partner.type", string="Partner Type")
    area_id = fields.Many2one("res.partner.area", string="Area")
    # Boolean
    home_consumption = fields.Boolean(string="Home Consumption")
    out_home_consumption = fields.Boolean(string="Out-Of-Home Consumption")

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        res = super().fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)
        if view_type == 'form':
            if not self.env.user.has_group('account.group_account_manager'):
                # make readonly
                doc = etree.XML(res['arch'])
                for node in doc.xpath("//field[@name='area_id']"):
                    node.set('force_save', '1')
                    modifiers = json.loads(node.get("modifiers"))
                    modifiers['readonly'] = True
                    node.set("modifiers", json.dumps(modifiers))
                res['arch'] = etree.tostring(doc)
        return res

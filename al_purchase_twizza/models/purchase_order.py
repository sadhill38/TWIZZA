from odoo import models, api
import logging
import json
from lxml import etree

_logger = logging.getLogger(__name__)


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    @api.onchange('picking_type_id')
    def _onchange_picking_type_id(self):
        if self.picking_type_id.default_location_dest_id.usage != 'customer':
            self.dest_address_id = False
            self.order_line.write({
                'account_analytic_id': self.picking_type_id.analytic_account_id.id or False
            })
        else:   # Dropship operation
            for line in self.order_line:
                line.account_analytic_id = line.sale_order_id.team_id.analytic_account_id.id or False

    @staticmethod
    def modifier_set_readonly(res, expression):
        doc = etree.XML(res['arch'])
        for node in doc.xpath(expression):
            node.set('force_save', '1')
            modifiers = json.loads(node.get("modifiers"))
            modifiers['readonly'] = True
            node.set("modifiers", json.dumps(modifiers))
        res['arch'] = etree.tostring(doc)

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        res = super().fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)
        if view_type == 'form':
            has_price_unit_access = self.env.user.has_group('al_purchase_twizza.group_purchase_unit_price_access')
            res_line_form = res['fields']['order_line']['views']['form']
            res_line_tree = res['fields']['order_line']['views']['tree']
            if not has_price_unit_access:
                self.modifier_set_readonly(res=res_line_form, expression="//field[@name='price_unit']")
                self.modifier_set_readonly(res=res_line_tree, expression="//field[@name='price_unit']")
        return res


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    @api.model
    def create(self, values):
        line = super(PurchaseOrderLine, self).create(values)
        if line.order_id.picking_type_id.default_location_dest_id.usage != 'customer':
            line.account_analytic_id = line.order_id.picking_type_id.analytic_account_id.id or False
        else:
            line.account_analytic_id = line.sale_order_id.team_id.analytic_account_id.id or False
        return line


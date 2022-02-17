from odoo import models, api
import logging

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


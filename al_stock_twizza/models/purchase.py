from odoo import fields, models, api, exceptions, _
import logging

_logger = logging.getLogger(__name__)


class PurchaseOrderLineInherit(models.Model):
    _inherit = "purchase.order.line"

    is_sample = fields.Boolean(string="Sample ?", default=False)

    @api.onchange('is_sample')
    def _onchange_is_sample(self):
        for rec in self:
            if rec.is_sample:
                rec.price_unit = 0.0
            else:
                rec._onchange_quantity()

    @api.onchange('product_qty', 'product_uom')
    def _onchange_quantity(self):
        self.is_sample = False
        return super(PurchaseOrderLineInherit, self)._onchange_quantity()

    def _prepare_stock_moves(self, picking):
        res = super(PurchaseOrderLineInherit, self)._prepare_stock_moves(picking)
        for dic in res:
            warehouse_id = self.order_id.picking_type_id.warehouse_id
            dic.update({
                'is_sample': self.is_sample,
                'location_dest_id': warehouse_id.sample_loc_id.id if (self.is_sample and warehouse_id.sample_loc_id) else warehouse_id.lot_stock_id.id,
            })
        return res

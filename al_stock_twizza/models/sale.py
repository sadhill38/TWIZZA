from odoo import fields, models, api, exceptions, _
import logging

_logger = logging.getLogger(__name__)


class SaleOrderLineInherit(models.Model):
    _inherit = "sale.order.line"

    is_sample = fields.Boolean(string="Sample ?", default=False)

    # def _get_reference_uom(self, uom):
    #     ref_uom = self.env['uom.uom'].search([
    #         ('category_id', '=', uom.category_id.id),
    #         ('uom_type', '=', 'reference')
    #     ])
    #     if len(ref_uom) == 1:
    #         return ref_uom
    #     else:
    #         return uom

    @api.onchange('is_sample')
    def _onchange_is_sample(self):
        for rec in self:
            if rec.is_sample:
                rec.price_unit = 0.0
                rec.purchase_price = 0.0
                rec.name += _(" (Sample)")
                # rec.product_uom = self._get_reference_uom(uom=rec.product_uom).id,
            else:
                rec.product_id_change()

    @api.onchange('product_uom', 'product_uom_qty')
    def product_uom_change(self):
        self.is_sample = False
        return super(SaleOrderLineInherit, self).product_uom_change()

    def _prepare_procurement_values(self, group_id):
        res = super(SaleOrderLineInherit, self)._prepare_procurement_values(group_id)
        # stock_customer = self.order_id.partner_id.property_stock_customer or False
        res.update({
            'is_sample': self.is_sample,
        })
        return res

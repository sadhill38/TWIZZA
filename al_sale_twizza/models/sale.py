# -*- coding: utf-8 -*-
from odoo import models, api, fields, exceptions, _
import logging

_logger = logging.getLogger(__name__)


class SaleOrderLineInherit(models.Model):
    _inherit = 'sale.order.line'

    product_category_id = fields.Many2one('product.category', string="Product Category", related='product_id.categ_id', readonly=True, store=True)
    total_purchase_price = fields.Float(string="Total cost", compute="_compute_cost", store=True, digits='Product Price')

    # def action_compute_purchase_price(self):
    #     for rec in self.env['sale.order.line'].search([]):
    #         rec.write(self._get_purchase_price(
    #             rec.order_id.pricelist_id,
    #             rec.product_id,
    #             rec.product_uom,
    #             fields.Date.context_today(self)
    #         ))

    @api.depends('product_uom_qty', 'purchase_price')
    def _compute_cost(self):
        for rec in self:
            rec.total_purchase_price = rec.product_uom_qty * rec.purchase_price

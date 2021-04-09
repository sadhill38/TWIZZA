# -*- coding: utf-8 -*-
from odoo import models, api, fields, exceptions, _
import logging

_logger = logging.getLogger(__name__)


class SaleOrderLineInherit(models.Model):
    _inherit = 'sale.order.line'

    product_category_id = fields.Many2one('product.category', string="Product Category", related='product_id.categ_id', readonly=True, store=True)
    total_purchase_price = fields.Float(string="Total cost", compute="_compute_cost", store=True, digits='Product Price')
    margin_invoiced = fields.Float(string='Margin Invoiced', compute='_product_margin_invoiced', digits='Product Price', store=True)

    # def action_compute_purchase_price(self):
    #     for rec in self.env['sale.order.line'].search([]):
    #         rec.write(self._get_purchase_price(
    #             rec.order_id.pricelist_id,
    #             rec.product_id,
    #             rec.product_uom,
    #             fields.Date.context_today(self)
    #         ))

    @api.depends('product_id', 'purchase_price', 'qty_invoiced', 'price_unit', 'untaxed_amount_invoiced')
    def _product_margin_invoiced(self):
        for line in self:
            currency = line.order_id.pricelist_id.currency_id
            price = line.purchase_price
            margin_invoiced = line.untaxed_amount_invoiced - (price * line.qty_invoiced)
            line.margin_invoiced = currency.round(margin_invoiced) if currency else margin_invoiced

    @api.depends('product_uom_qty', 'purchase_price')
    def _compute_cost(self):
        for rec in self:
            rec.total_purchase_price = rec.product_uom_qty * rec.purchase_price

# -*- coding: utf-8 -*-
from odoo import models, api, fields, exceptions, _
import logging

_logger = logging.getLogger(__name__)


class SaleOrderLineInherit(models.Model):
    _inherit = 'sale.order.line'

    service_rate = fields.Float(string="Service Rate (%)", compute="_compute_rates", store=True, group_operator='avg')
    margin_rate = fields.Float(string="Margin Rate (%)", compute="_compute_rates", store=True, group_operator='avg')
    product_category_id = fields.Many2one('product.category', string="Product Category", related='product_id.categ_id',
                                          readonly=True, store=True)

    @api.depends('qty_delivered', 'product_uom_qty', 'product_id', 'product_id.standard_price', 'price_unit')
    def _compute_rates(self):
        for rec in self:
            service_rate = 0.0
            margin_rate = 0.0
            if rec.product_uom_qty != 0.0:
                service_rate = (rec.qty_delivered / rec.product_uom_qty) * 100
            rec.service_rate = service_rate
            if rec.product_id and rec.product_id.standard_price > 0.0:
                unit_cost = rec.product_id.standard_price
                margin_rate = ((rec.price_unit - unit_cost) * 100) / unit_cost
            rec.margin_rate = margin_rate

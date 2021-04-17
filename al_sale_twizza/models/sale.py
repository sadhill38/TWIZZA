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

    @api.depends('product_uom_qty', 'purchase_price', 'order_id.currency_id')
    def _compute_cost(self):
        for rec in self:
            total_cost = rec.product_uom_qty * rec.purchase_price
            rec.total_purchase_price = rec.order_id.currency_id.round(total_cost)


class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    days_to_confirm = fields.Float(string='Days to confirm', compute='_compute_days_to', store=True)
    days_to_invoice = fields.Float(string='Days to invoice', compute='_compute_days_to', store=True)

    @api.depends('create_date', 'date_order', 'state', 'invoice_ids', 'invoice_ids.invoice_date')
    def _compute_days_to(self):
        for rec in self:
            rec.days_to_confirm = (rec.date_order - rec.create_date).days if rec.state in ['sale', 'done'] else 0.0
            delivered_dates = self.env['stock.picking'].search([
                ('sale_id', '=', rec.id),
                ('state', 'in', ['done'])
            ]).mapped('date_done')
            invoiced_dates = rec.invoice_ids.filtered(lambda x: x.state in ['posted']).mapped('invoice_date')
            days_to_invoice = 0.0
            if rec.state in ['sale', 'done'] and delivered_dates and invoiced_dates:
                days_to_invoice = (max(invoiced_dates) - max(delivered_dates).date()).days
            rec.days_to_invoice = days_to_invoice

# -*- coding: utf-8 -*-
from odoo import models, api, fields, exceptions, _
import json
from lxml import etree
# from odoo.tools.safe_eval import safe_eval
import logging

_logger = logging.getLogger(__name__)


class SaleOrderLineInherit(models.Model):
    _inherit = 'sale.order.line'

    product_category_id = fields.Many2one('product.category', string="Product Category", related='product_id.categ_id', readonly=True, store=True)
    total_purchase_price = fields.Float(string="Total cost", compute="_compute_cost", store=True, digits='Product Price')
    margin_invoiced = fields.Float(string='Margin Invoiced', compute='_product_margin_invoiced', digits='Product Price', store=True)
    # add groups sale_manager
    purchase_price = fields.Float(string='Cost', digits='Product Price', groups="sales_team.group_sale_manager")

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

    @staticmethod
    def modifier_set_readonly(res, expression):
        doc = etree.XML(res['arch'])
        for node in doc.xpath(expression):
            modifiers = json.loads(node.get("modifiers"))
            modifiers['readonly'] = True
            node.set("modifiers", json.dumps(modifiers))
        res['arch'] = etree.tostring(doc)

    # @staticmethod
    # def modifier_set_invisible(res, expression):
    #     doc = etree.XML(res['arch'])
    #     for node in doc.xpath(expression):
    #         modifiers = json.loads(node.get("modifiers"))
    #         modifiers['invisible'] = True
    #         node.set("modifiers", json.dumps(modifiers))
    #     res['arch'] = etree.tostring(doc)

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        res = super(SaleOrderInherit, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)
        if view_type == 'form':
            is_admin_sales = self.env.user.has_group('sales_team.group_sale_manager')
            if not is_admin_sales:
                xpath = "//field[@name='discount' or @name='price_unit']"
                # xpath2 = "//field[@name='purchase_price']"
                res_line_form = res['fields']['order_line']['views']['form']
                res_line_tree = res['fields']['order_line']['views']['tree']
                self.modifier_set_readonly(res=res_line_form, expression=xpath)
                # self.modifier_set_invisible(res=res_line_form, expression=xpath2)
                self.modifier_set_readonly(res=res_line_tree, expression=xpath)
        return res

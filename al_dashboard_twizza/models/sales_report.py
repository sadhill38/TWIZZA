# -*- coding: utf-8 -*-
from odoo import models, api, fields, tools, _
import logging

_logger = logging.getLogger(__name__)


class DirectionSalesReport(models.Model):
    _name = "twizza.sales.report"
    _description = "Twizza Sales Report"
    _auto = False
    _rec_name = 'date'
    _order = 'date desc'

    # @api.model
    # def _get_done_states(self):
    #     return ['sale', 'done', 'paid']

    # Measures
    product_uom_qty = fields.Float(string='Qty Ordered', readonly=True)
    qty_delivered = fields.Float(string='Qty Delivered', readonly=True)
    # qty_to_invoice = fields.Float(string='Qty To Invoice', readonly=True)
    qty_invoiced = fields.Float(string='Qty Invoiced', readonly=True)
    price_subtotal = fields.Float(string='Untaxed Total', readonly=True)
    subtotal_nodiscount = fields.Float(string='Subtotal (No Discount)', readonly=True)
    price_total = fields.Float(string='Total', readonly=True)
    margin = fields.Float(string='Margin', readonly=True)
    margin_invoiced = fields.Float(string='Margin Invoiced', readonly=True)
    # untaxed_amount_to_invoice = fields.Float(string='Untaxed Amount To Invoice', readonly=True)
    untaxed_amount_invoiced = fields.Float(string='Untaxed Amount Invoiced', readonly=True)
    nbr = fields.Integer(string='# of Lines', readonly=True)
    # discount = fields.Float(string='Discount %', readonly=True)
    discount_amount = fields.Float(string='Discount Amount', readonly=True)
    weight = fields.Float(string='Gross Weight', readonly=True)
    weight_delivered = fields.Float(string='Weight Delivered', readonly=True)

    # volume = fields.Float(string='Volume', readonly=True)
    days_to_confirm = fields.Float(string='Days To Confirm', readonly=True, group_operator="avg")
    days_to_invoice = fields.Float(string='Days To Invoice', readonly=True, group_operator="avg")
    total_purchase_price = fields.Float(string="Total cost", readonly=True)
    price_tax = fields.Float(string='Total Tax', readonly=True)
    # Col/Row
    name = fields.Char(string='Order Reference', readonly=True)
    date = fields.Datetime(string='Order Date', readonly=True)
    product_id = fields.Many2one('product.product', string='Product Variant', readonly=True)
    product_uom = fields.Many2one('uom.uom', string='Unit of Measure', readonly=True)
    partner_id = fields.Many2one('res.partner', string='Customer', readonly=True)
    created_by = fields.Many2one('res.users', string='Created by', readonly=True)
    company_id = fields.Many2one('res.company', string='Company', readonly=True)
    user_id = fields.Many2one('res.users', string='Salesperson', readonly=True)
    product_tmpl_id = fields.Many2one('product.template', string='Product', readonly=True)
    categ_id = fields.Many2one('product.category', string='Product Category', readonly=True)
    pricelist_id = fields.Many2one('product.pricelist', string='Pricelist', readonly=True)
    # analytic_account_id = fields.Many2one('account.analytic.account', string='Analytic Account', readonly=True)
    team_id = fields.Many2one('crm.team', string='Sales Team', readonly=True)
    country_id = fields.Many2one('res.country', string='Customer Country', readonly=True)
    # industry_id = fields.Many2one('res.partner.industry', string='Customer Industry', readonly=True)
    commercial_partner_id = fields.Many2one('res.partner', string='Customer Entity', readonly=True)
    warehouse_id = fields.Many2one('stock.warehouse', string='Warehouse', readonly=True)
    route_id = fields.Many2one('stock.location.route', string='Route', readonly=True)
    state = fields.Selection([
        ('draft', 'Draft Quotation'),
        ('sent', 'Quotation Sent'),
        ('sale', 'Sales Order'),
        ('done', 'Sales Done'),
        ('cancel', 'Cancelled'),
        ], string='Status', readonly=True)
    invoice_status = fields.Selection([
        ('upselling', 'Upselling Opportunity'),
        ('invoiced', 'Fully Invoiced'),
        ('to invoice', 'To Invoice'),
        ('no', 'Nothing to Invoice')
    ], string="Invoice Status", readonly=True)
    # campaign_id = fields.Many2one('utm.campaign', string='Campaign', readonly=True)
    # medium_id = fields.Many2one('utm.medium', string='Medium', readonly=True)
    # source_id = fields.Many2one('utm.source', string='Source', readonly=True)
    order_id = fields.Many2one('sale.order', string='Order #', readonly=True)

    @staticmethod
    def _query(with_clause='', fields={}, groupby='', from_clause=''):
        """
        l = sale_order_line
        s = sale_order
        partner = res_partner
        p = product_product
        t = product_template
        u = uom_uom on (u.id=l.product_uom)
        u2 = uom_uom on (u2.id=t.uom_id)
        pp = product_pricelist
        """
        with_ = ("WITH %s" % with_clause) if with_clause else ""

        select_ = """
            min(l.id) as id,
            l.product_id as product_id,
            t.uom_id as product_uom,
            sum(l.product_uom_qty / u.factor * u2.factor) as product_uom_qty,
            sum(l.qty_delivered / u.factor * u2.factor) as qty_delivered,
            sum(l.qty_invoiced / u.factor * u2.factor) as qty_invoiced,
            sum(l.price_total / CASE COALESCE(s.currency_rate, 0) WHEN 0 THEN 1.0 ELSE s.currency_rate END) as price_total,
            sum(l.price_subtotal / CASE COALESCE(s.currency_rate, 0) WHEN 0 THEN 1.0 ELSE s.currency_rate END) as price_subtotal,
            sum(l.price_unit * l.product_uom_qty / CASE COALESCE(s.currency_rate, 0) WHEN 0 THEN 1.0 ELSE s.currency_rate END) as subtotal_nodiscount,
            sum(l.untaxed_amount_invoiced / CASE COALESCE(s.currency_rate, 0) WHEN 0 THEN 1.0 ELSE s.currency_rate END) as untaxed_amount_invoiced,
            sum(l.total_purchase_price / CASE COALESCE(s.currency_rate, 0) WHEN 0 THEN 1.0 ELSE s.currency_rate END) as total_purchase_price,
            sum(l.margin / CASE COALESCE(s.currency_rate, 0) WHEN 0 THEN 1.0 ELSE s.currency_rate END) as margin,
            sum(l.margin_invoiced / CASE COALESCE(s.currency_rate, 0) WHEN 0 THEN 1.0 ELSE s.currency_rate END) as margin_invoiced,
            sum(l.price_tax / CASE COALESCE(s.currency_rate, 0) WHEN 0 THEN 1.0 ELSE s.currency_rate END) as price_tax,
            count(*) as nbr,
            s.name as name,
            s.date_order as date,
            s.state as state,
            s.partner_id as partner_id,
            s.create_uid as created_by,
            s.user_id as user_id,
            s.company_id as company_id,
            t.categ_id as categ_id,
            s.pricelist_id as pricelist_id,
            s.team_id as team_id,
            s.warehouse_id as warehouse_id,
            s.invoice_status as invoice_status,
            p.product_tmpl_id,
            partner.country_id as country_id,
            partner.commercial_partner_id as commercial_partner_id,
            sum(p.weight * l.product_uom_qty / u.factor * u2.factor) as weight,
            sum(p.weight * l.qty_delivered / u.factor * u2.factor) as weight_delivered,
            l.route_id as route_id,
            sum((l.price_unit * l.product_uom_qty * l.discount / 100.0 / CASE COALESCE(s.currency_rate, 0) WHEN 0 THEN 1.0 ELSE s.currency_rate END)) as discount_amount,
            s.days_to_confirm as days_to_confirm,
            s.days_to_invoice as days_to_invoice,
            s.id as order_id
        """

        for field in fields.values():
            select_ += field

        from_ = """
                sale_order_line l 
                    join sale_order s on (l.order_id=s.id)
                        join res_partner partner on (s.partner_id = partner.id)
                            left join product_product p on (l.product_id=p.id)
                            left join product_template t on (p.product_tmpl_id=t.id)
                    left join uom_uom u on (u.id=l.product_uom)
                    left join uom_uom u2 on (u2.id=t.uom_id)
                    left join product_pricelist pp on (s.pricelist_id = pp.id)
                %s
        """ % from_clause

        groupby_ = """
            l.product_id,
            l.order_id,
            t.uom_id,
            t.categ_id,
            s.name,
            s.date_order,
            s.partner_id,
            s.create_uid,
            s.user_id,
            s.state,
            s.company_id,
            s.pricelist_id,            
            s.team_id,
            s.warehouse_id,
            s.invoice_status,
            p.product_tmpl_id,
            partner.country_id,
            partner.commercial_partner_id,
            l.route_id,
            s.id %s
        """ % groupby

        return '%s (SELECT %s FROM %s WHERE l.product_id IS NOT NULL GROUP BY %s)' % (with_, select_, from_, groupby_)

    def init(self):
        # self._table = sale_report
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""CREATE or REPLACE VIEW %s as (%s)""" % (self._table, self._query()))

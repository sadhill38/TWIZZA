# -*- coding: utf-8 -*-
from odoo import models, fields, _
import logging

_logger = logging.getLogger(__name__)


class ProductTemplateInherit(models.Model):
    _inherit = "product.template"

    standard_price = fields.Float(
        'Cost', company_dependent=True,
        digits='Product Price',
        groups="al_product_twizza.group_product_cost_management",
        help="""In Standard Price & AVCO: value of the product (automatically computed in AVCO).
            In FIFO: value of the last unit that left the stock (automatically computed).
            Used to value the product when the purchase cost is not known (e.g. inventory adjustment).
            Used to compute margins on sale orders.""")


class ProductProductInherit(models.Model):
    _inherit = "product.product"

    standard_price = fields.Float(
        'Cost', company_dependent=True,
        digits='Product Price',
        groups="al_product_twizza.group_product_cost_management",
        help="""In Standard Price & AVCO: value of the product (automatically computed in AVCO).
            In FIFO: value of the last unit that left the stock (automatically computed).
            Used to value the product when the purchase cost is not known (e.g. inventory adjustment).
            Used to compute margins on sale orders.""")

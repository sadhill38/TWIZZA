from odoo import fields, models, api, exceptions, _
import logging

_logger = logging.getLogger(__name__)


class StockWarehouseInherit(models.Model):
    _inherit = "stock.warehouse"

    sample_loc_id = fields.Many2one('stock.location', string='Sample Location', required=True, check_company=True,
                                    domain="[('usage', '=', 'internal'), ('company_id', '=', company_id)]")

    def _get_locations_values(self, vals, code=False):
        res = super(StockWarehouseInherit, self)._get_locations_values(vals, code)
        code = vals.get('code') or code or ''
        code = code.replace(' ', '').upper()
        company_id = vals.get('company_id', self.default_get(['company_id'])['company_id'])
        res.update({
            'sample_loc_id': {
                'name': _('Samples'),
                'active': True,
                'usage': 'internal',
                'barcode': self._valid_barcode(code + '-SAMPLE', company_id)
            },
        })
        return res


class StockMoveInherit(models.Model):
    _inherit = "stock.move"

    is_sample = fields.Boolean(string="Sample ?", default=False)

    def _prepare_move_line_vals(self, quantity=None, reserved_quant=None):
        res = super(StockMoveInherit, self)._prepare_move_line_vals(quantity, reserved_quant)
        move_id = self.env['stock.move'].browse(res['move_id'])
        res.update({
            'is_sample': move_id.is_sample,
            'location_id': move_id.location_id.id,
            'location_dest_id': move_id.location_dest_id._get_putaway_strategy(move_id.product_id).id or move_id.location_dest_id.id,
        })
        _logger.info("******** _prepare_move_line_vals ********")
        _logger.info(res)
        _logger.info(move_id.location_id)
        _logger.info(move_id.location_dest_id)
        _logger.info("*****************************************")
        return res

    def _create_in_svl(self, forced_quantity=None):
        res = super(StockMoveInherit, self)._create_in_svl(forced_quantity)
        for sm in self:
            svl = res.filtered(lambda x: x.product_id.id == sm.product_id.id and x.stock_move_id.id == sm.id)
            if sm.is_sample and svl:
                svl.update({
                    'unit_cost': sm.price_unit,
                    'is_sample': sm.is_sample,
                    'value': sm.price_unit * (forced_quantity or sm.quantity_done),
                })
        return res

    def _create_out_svl(self, forced_quantity=None):
        res = super(StockMoveInherit, self)._create_out_svl(forced_quantity)
        for sm in self:
            svl = res.filtered(lambda x: x.product_id.id == sm.product_id.id and x.stock_move_id.id == sm.id)
            if sm.is_sample and svl:
                svl.update({
                    'unit_cost': sm.price_unit,
                    'is_sample': sm.is_sample,
                    'value': sm.price_unit * (forced_quantity or sm.quantity_done),
                })
        return res


class StockMoveLineInherit(models.Model):
    _inherit = "stock.move.line"

    is_sample = fields.Boolean(string="Sample ?", default=False)


class StockValuationLayerInherit(models.Model):
    _inherit = "stock.valuation.layer"

    is_sample = fields.Boolean(string="Sample ?", default=False, readonly=True)


class StockRuleInherit(models.Model):
    _inherit = 'stock.rule'

    def _get_stock_move_values(self, product_id, product_qty, product_uom, location_id, name, origin, values, group_id):
        res = super(StockRuleInherit, self)._get_stock_move_values(product_id, product_qty, product_uom, location_id, name, origin, values, group_id)
        warehouse_id = group_id.get('warehouse_id', False)
        is_sample = group_id.get('is_sample', False)
        res.update({
            'is_sample': is_sample,
            'location_id': warehouse_id.sample_loc_id.id if (is_sample and warehouse_id.sample_loc_id) else self.location_src_id.id,
        })
        _logger.info(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        _logger.info(res)
        _logger.info(group_id)
        _logger.info(location_id)
        _logger.info(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        return res

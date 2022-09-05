from odoo import fields, models, api, _
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_round
from odoo.addons.base.models import decimal_precision as dp


class Returns(models.Model):
    _name = "stocks.return"
    _rec_name = "date_order"

    @api.model
    def _get_default_team(self):
        return self.env['crm.team']._get_default_team_id()

    name = fields.Char('Return Reference', required=True, index=True, copy=False, default='Nouveau Bon de Sortie')
    project_name = fields.Char(String='Nom projet')
    company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env.user.company_id.id)
    pricelist_id = fields.Many2one(
        'product.pricelist', string='Pricelist', check_company=True,  # Unrequired company
        readonly=True,
        help="If you change the pricelist, only newly added lines will be affected.")
    partner_shipping_id = fields.Many2one(
        'res.partner', string='Delivery Address', readonly=True,
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]", )
    date_exp = fields.Date(string='Date Expiration')
    name_seq = fields.Char(string='Bon de sortie', required=True, copy=False,
                           readonly=True, index=True, default=lambda self: _('New'))

    date_order = fields.Date(string='Order Date')
    partner_id = fields.Many2one('res.partner', string='Customer')
    amount_total = fields.Monetary(string='Total', store=True, readonly=True),  # compute='_amount_all'
    is_delivered = fields.Boolean(string="Is Delivered?", default=False, copy=False)
    user_id = fields.Many2one('res.users', string='Return Representative', default=lambda self: self.env.user.id)
    location_id = fields.Many2one('stock.location', string='Location')  # compute='_compute_location'
    picking_id = fields.Many2one('stock.picking', string='Picking', copy=False)
    # invoice_id = fields.Many2one('account.invoice', string='Invoice', copy=False)
    # company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env.user.company_id.id)
    # return_line_ids = fields.One2many('stocks.return.line', 'return_id', string='Order Lines',
    #                                   copy=True)

    return_line_ids = fields.One2many('stocks.return.line','return_id')

class ReturnLines(models.Model):
    _name = "stocks.return.line"
    name = fields.Text(string='Description')
    product_qty = fields.Float(string='Quantity', digits=dp.get_precision('Product Unit of Measure'))
    # tax_ids = fields.Many2many('account.tax', string='Taxes',
    #                            domain=['|', ('active', '=', False), ('active', '=', True)])
    product_uom = fields.Many2one('uom.uom', string='Product Unit of Measure')
    # product_id = fields.Many2one('product.product', string='Product', domain=[('sale_ok', '=', True)],
    #                              change_default=True)
    price_unit = fields.Float(string='Unit Price', digits=dp.get_precision('Product Price'))
    # price_subtotal = fields.Monetary(string='Total', store=True)  # compute='_compute_amount',
    # price_total = fields.Monetary(string='Total', store=True)  # compute='_compute_amount',
    # price_tax = fields.Float(string='Tax', store=True)  # compute='_compute_amount',
    return_id = fields.Many2one('stocks.return', string='Order Reference', index=True,
                                ondelete='cascade')
    # account_analytic_id = fields.Many2one('account.analytic.account', string='Analytic Account')
    # analytic_tag_ids = fields.Many2many('account.analytic.tag', string='Analytic Tags')
    # state = fields.Selection(store=True, readonly=False) # related='return_id.state',
    # currency_id = fields.Many2one(store=True, string='Currency', readonly=True)  # related='return_id.currency_id',
    # partner_id = fields.Many2one('res.partner', related='return_id.partner_id', string='Partner', readonly=True,
    #                              store=True)  # related='return_id.partner_id',
    date_order = fields.Date(string='Order Date', readonly=True)  # related='return_id.date_order',
    # company_id = fields.Many2one('res.company', 'Company', store=True)  # related='return_id.company_id',

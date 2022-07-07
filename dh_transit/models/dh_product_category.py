from odoo import models, fields, api


class DhProductCategory(models.Model):
    _inherit = 'product.category'

    est_charge_client = fields.Boolean(string='Est charge client?')
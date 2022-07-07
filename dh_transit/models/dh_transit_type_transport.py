from odoo import models, fields, api


class DhTransitTypeTransport(models.Model):
    _name = 'dh.transit.type.transport'

    name = fields.Char(string='Nom')
    mode_id = fields.Many2one('dh.transit.mode.transport', string='Mode')
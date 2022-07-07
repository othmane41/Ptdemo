from odoo import models, fields, api


class DhTransitModeTransport(models.Model):
    _name = 'dh.transit.mode.transport'

    name = fields.Char(string='Nom')
    description = fields.Char(string='Description')
    type_transport_ids = fields.One2many('dh.transit.type.transport', 'mode_id', string='Types transport', domain=lambda self: [('mode_id', '=', self.id)])
    is_maritime = fields.Boolean(string='Est maritime?')


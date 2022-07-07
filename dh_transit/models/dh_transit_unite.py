from odoo import models, fields, api

class DhTransitUnite(models.Model):
    _name = 'dh.transit.unite'
    _rec_name = 'type_unite'

    type_unite = fields.Char(string='Type')
    sous_type_unite = fields.One2many('dh.transit.sous.unite', 'unit_type_id', string='Sous Types')

class DhTransitSousUnite(models.Model):
    _name = 'dh.transit.sous.unite'
    _rec_name = 'type_unite'

    type_unite = fields.Char(string='Type')
    unit_type_id = fields.Many2one('dh.transit.unite', string='Type')
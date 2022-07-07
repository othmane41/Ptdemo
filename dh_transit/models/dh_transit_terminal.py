from odoo import models, fields, api

class DhTransitTerminal(models.Model):
    _name = 'dh.transit.terminal'
    _rec_name = 'nom'
    nom = fields.Char(string='Terminal')
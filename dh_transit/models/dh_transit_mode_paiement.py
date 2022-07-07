from odoo import models, fields, api


class DhModePaiement(models.Model):
    _name = 'dh.transit.mode.paiement'
    _rec_name = 'mode_paiment'

    mode_paiment=fields.Char(string="Mode de paiement")
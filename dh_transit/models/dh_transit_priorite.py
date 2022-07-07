from odoo import models, fields, api


class DhTransitpriorite(models.Model):
    _name = 'dh.transit.priorite'
    _rec_name = 'priorite'
    priorite = fields.Char(string='Priorité', tracking=True)









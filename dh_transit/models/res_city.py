from odoo import models, fields, api

class DhResCity(models.Model):
    _name = 'res.city'
    _rec_name = 'nom'

    nom = fields.Char(string='ville')
    dh_country_id=fields.Many2one('res.country', string='country')
    dh_partner_ville_id=fields.Many2one('res.partner', string='country')
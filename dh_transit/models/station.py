from odoo import models, fields, api

class DhResCity(models.Model):
    _name = 'dh.station'
    _rec_name = 'nom'

    nom = fields.Char(string='N° Station / Projet')

from odoo import models, fields, api

class Dhcontenant(models.Model):
    _name = 'dh.contenant'
    _rec_name = 'nom'

    nom = fields.Char(string='Nbre de contenant')

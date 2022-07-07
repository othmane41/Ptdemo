from odoo import models, fields, api


class DhTypeInterlocuteur(models.Model):
    _name = 'dh.type.interlocuteur'
    _rec_name = 'type'

    type = fields.Char(string='Type')
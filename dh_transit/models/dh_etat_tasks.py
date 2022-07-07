from odoo import models, fields, api


class DhEtatTasks(models.Model):
    _name = 'dh.etat.tasks'

    name = fields.Char(string='Nom')
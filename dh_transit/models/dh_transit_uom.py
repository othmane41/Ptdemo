from odoo import models, fields, api


class DhUOM(models.Model):
    _name = 'dh.transit.uom'
    _rec_name = 'code_unite'

    code_unite= fields.Char(string='Code_Unite', tracking=True)
    intitule_unite= fields.Char(string='Intitule_Unite', tracking=True)
    type_colis= fields.Char(string='Type de colis', tracking=True)







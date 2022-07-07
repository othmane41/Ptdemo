from odoo import models, fields, api

class Dhtransitefacturelines(models.Model):
    _name = 'dh.transite.facture.lines'


    code_ngp = fields.Char(string='Code NGP', tracking=True)
    code_article_expediteur = fields.Char(string='Code Article Expéditeur', tracking=True)
    code_article_destinataire = fields.Char(string='Code Article Destinataire', tracking=True)
    designation_commerciale = fields.Char(string='Désignation', tracking=True)
    unite_mesure = fields.Many2one('dh.transit.uom', string='Unité de mesure', tracking=True)
    quantite = fields.Float(string='Quantité ', tracking=True)
    poids_net = fields.Float(string='Poids Net', tracking=True)
    valeur = fields.Float(string='Valeur', tracking=True)
    code_pays_id=fields.Many2one('res.country', string='Code pays', tracking=True)
    dh_transit_facture_id=fields.Many2one('dh.transit.facture', string='Facture', tracking=True)






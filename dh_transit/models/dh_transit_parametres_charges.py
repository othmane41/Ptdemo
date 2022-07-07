from odoo import models, fields, api


class DhTransitParametresCharrge(models.Model):
    _name = 'dh.transit.parametres.charges'

    name = fields.Char(string='Nom')
    type_declaration = fields.Selection(
        [('normale', 'Normale'), ('nouvelle', 'Nouvelle provisionnelle'), ('occasionnelle', 'Occasionnelle'),
         ('dum_combinee', 'DUM combinée'), ('dum_anticipee', 'DUM anticipée')], string='Type déclaration',
        tracking=True)
    code_bureau_dedouanement = fields.Many2one('dh.transit.bureau', string='Bureau dédouanement',
                                               tracking=True)  # Code Bureau dédouanement
    code_regime = fields.Many2one('dh.transit.regime', string='Régime', tracking=True)  # Code régime
    code_bureau_destination = fields.Many2one('dh.transit.bureau', string='Bureau destination',
                                              tracking=True)  # Code Bureau destination
    client_id = fields.Many2one('res.partner', string="Client")
    parametres_charges_line_ids = fields.One2many('dh.transit.parametres.charges.line', 'parametres_charges_id', string='Lignes de parametres charges')





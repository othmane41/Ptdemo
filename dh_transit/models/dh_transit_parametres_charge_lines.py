from odoo import models, fields, api


class DhTransitParametresCharrgeLine(models.Model):
    _name = 'dh.transit.parametres.charges.line'



    product_id = fields.Many2one('product.product', string="Article",domain="[('purchase_ok', '=', True)]")
    prix = fields.Float(string='Prix', tracking=True)
    parametres_charges_id = fields.Many2one('dh.transit.parametres.charges', string="charges_id")
    type_declaration = fields.Selection([('normale', 'Normale'), ('nouvelle', 'Nouvelle provisionnelle'), ('occasionnelle', 'Occasionnelle'),('dum_combinee', 'DUM combinée'), ('dum_anticipee', 'DUM anticipée')], string='Type déclaration',related='parametres_charges_id.type_declaration')
    code_bureau_dedouanement = fields.Many2one('dh.transit.bureau', string='Bureau dédouanement',related='parametres_charges_id.code_bureau_dedouanement')
    code_regime = fields.Many2one('dh.transit.regime', string='Régime', related='parametres_charges_id.code_regime')
    code_bureau_destination = fields.Many2one('dh.transit.bureau', string='Bureau destination',
                                              related='parametres_charges_id.code_bureau_destination')
    client_id = fields.Many2one('res.partner', string="Client", related='parametres_charges_id.client_id',store=True)
    name = fields.Char(string='Nom',related='parametres_charges_id.name')






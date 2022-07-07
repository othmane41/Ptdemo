from odoo import models, fields, api


class DhTransitParametreAnnexation(models.Model):
    _name = 'dh.transit.parametre.annexation'

    name = fields.Char(string='Nom')
    type_operation = fields.Selection(
        [('import', 'Import'), ('export', 'Export')], string='Type opération', tracking=True)
    code_bureau_dedouanement = fields.Many2one('dh.transit.bureau', string='Bureau dédouanement', tracking=True)
    mode_transport = fields.Many2one('dh.transit.mode.transport', string='Mode transport', tracking=True)
    type_transport = fields.Many2one('dh.transit.type.transport', string='Moyen de transport', tracking=True)
    code_regime = fields.Many2one('dh.transit.regime', string='Régime', tracking=True)
    code_bureau_destination = fields.Many2one('dh.transit.bureau', string='Bureau destination', tracking=True)
    annexation_lines = fields.One2many('dh.transit.parametre.annexation.lines', 'annexe_id', string='Lignes')

class DhTransitParametreAnnexationLines(models.Model):
    _name = 'dh.transit.parametre.annexation.lines'

    annexe_id = fields.Many2one('dh.transit.parametre.annexation', string='Annexe')
    type = fields.Many2one('dh.transit.type.annexation', string='Type')
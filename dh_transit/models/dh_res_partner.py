from odoo import models, fields, api


class DhResPartner(models.Model):
    _inherit = 'res.partner'

    prestation = fields.Char(string='Préstation')
    reference = fields.Char(string='Référence')

    ###################################################
    # Renseignement client (CRM)
    interlocuteur_ids = fields.Many2many('dh.type.interlocuteur', string='Types interlocuteurs')
    code_client=fields.Char(string='Code Client',readonly=True)
    code_sage=fields.Char(string='Code Sage',readonly=True)
    type_client=fields.Char(string='Type de client')
    ref_client=fields.Char(string='Réf Client')
    raison_sociale=fields.Char(string='Raison Sociale')
    Ville_id = fields.Many2one('res.city',string="Ville")
    n_rc=fields.Char('N° RC')
    n_centre_rc=fields.Char('N° Centre RC')
    ice=fields.Char('ICE')
    secteur_activite=fields.Selection([('industrie', 'Industrie'), ('agricole', 'Agricole'),('negoce', 'Négoce'),('autre', 'Autre')], string="Secteur d'activité", tracking=True)
    nbre_ops_prevues_mois=fields.Char(string="Nbre d'ops prévues / mois")
    bureau_dedouanement=fields.Many2one('dh.transit.bureau', string="Bureau de dédouanement")
    type_dedouanement= fields.Selection([('import', 'Import'), ('export', 'Export'),('consignation', 'Consignation')], string="Type de dédouanement", tracking=True)
    is_maritime = fields.Boolean(string="Est compagnie Maritime?")
    is_transporteur = fields.Boolean(string="Est Transporteur?")
    is_soumissionnaire = fields.Boolean(string="Est Soumissionnaire?")
    is_prestataire = fields.Boolean(string="Est Prestataire?")
    is_producteur = fields.Boolean(string="Est Producteur?")
    categories_ids = fields.Many2many('product.category', string='Categories')

    @api.model
    def create(self, vals):
        vals['code_client'] = self.env['ir.sequence'].next_by_code('res.partner.code.client')
        vals['code_sage'] = self.env['ir.sequence'].next_by_code('res.partner.code.sage')
        res = super().create(vals)
        return res





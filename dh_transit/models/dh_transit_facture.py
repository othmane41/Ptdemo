from odoo import models, fields, api


class DhFacture(models.Model):
    _name = 'dh.transit.facture'
    _rec_name = 'n_facture'

    n_facture = fields.Char(string='N° facture',tracking=True)
    poids_net = fields.Float(string='Poids Net', tracking=True)
    date_facture = fields.Date(string='Date de facture',tracking=True)
    fournisseur_id = fields.Many2one('res.partner', string='Expéditeur',tracking=True)
    station_id = fields.Many2one('dh.station', string='N° Station / Projet',tracking=True)
    destinatire_id = fields.Many2one('res.partner', string='Destinataire',tracking=True)
    producteur_id = fields.Many2one('res.partner', string='Producteur',tracking=True)

    incoterm = fields.Many2one('account.incoterms', string='Incoterm', tracking=True)
    mode_paiement = fields.Many2one('dh.transit.mode.paiement', string='Mode de paiement',tracking=True)
    quantite=fields.Float(string='Quantité ',tracking=True)
    prix_unitaire=fields.Float(string='Prix unitaire ',tracking=True)
    poids_brut_unitaire = fields.Float(string='Poids Brut unitaire', tracking=True)
    poids_net_unitaire = fields.Float(string='Poids Brut unitaire', tracking=True)
    unite_mesure= fields.Many2one('dh.transit.uom', string='Unité de mesure',tracking=True)
    code_devise= fields.Many2one('res.currency', string='Devise',tracking=True)
    rate = fields.Float(string='Cours de change', tracking=True)
    poids_brut_total=fields.Float(string='Poids Brut Total', tracking=True)
    poids_net_total=fields.Float(string='Poids Net Total', tracking=True)
    total_facture=fields.Float(string='Total facture',tracking=True)
    transit_dossier_id = fields.Many2one('dh.transit.dossier')
    contenant_id = fields.Many2one('dh.contenant',string='Nbre de contenant')
    dh_transit_facture_line_ids=fields.One2many('dh.transite.facture.lines','dh_transit_facture_id')


    # @api.model
    # def create(self, vals):
    #     vals['n_facture'] = self.env['ir.sequence'].next_by_code('dh.transit.facture')
    #     res = super().create(vals)
    #     return res


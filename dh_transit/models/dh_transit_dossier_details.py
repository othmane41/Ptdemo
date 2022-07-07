from odoo import models, fields, api


class DhTransitDossierDetails(models.Model):
    _name = 'dh.transit.dossier.details'

    # num_dossier = fields.Char(string='N° Dossier')
    # expediteur = fields.Many2one('res.partner', string='Expéditeur')
    # destinataire = fields.Many2one('res.partner', string='Destinataire')
    # type_declaration = fields.Selection([('normale', 'Normale'), ('nouvelle', 'Nouvelle provisionnelle'), ('occasionnelle', 'Occasionnelle'), ('dum_combinee', 'DUM combinée'), ('dum_anticipee', 'DUM anticipée')], string='Type déclaration')
    # article_id = fields.Many2one('product.template', string='Désignation marchandise')
    # origine_marchandise = fields.Many2one('res.country', string='Origine de la marchandise')
    # provenance = fields.Many2one('res.country', string='Provenance')
    # num_manifeste = fields.Char(string='N° Manifeste')
    # mode_transport = fields.Many2one('dh.transit.mode.transport', string='Mode transport')
    # is_maritime = fields.Boolean(string='Est maritime?', related='mode_transport.is_maritime')
    # type_transport = fields.Many2one('dh.transit.type.transport', string='Type transport')
    # type_transport_maritime = fields.Selection(
    #     [('conteneur', 'Conteneur'), ('cont_man_accom', 'Conteneur manifesté accompagné'),
    #      ('cont_man_non_accom', 'Conteneur manifesté non accompagné')], string='Type transport')
    # type_transport_routier = fields.Selection(
    #     [('camion', 'Camion'), ('ensemble', 'Ensemble routier'), ('remorque', 'Remorque'), ('tir', 'TIR')],
    #     string='Type transport')
    # type_transport_air = fields.Selection(
    #     [('air_freight', 'Air Freight'), ('bag_accom', 'Baggage accompagné'), ('charter', 'Charter')],
    #     string='Type transport')
    # type_transport_autre = fields.Selection([('engin_agricol', 'Engin Agricol'), ('engin_btp', 'Engin BTP')],
    #                                         string='Type transport')
    # transporteur = fields.Many2one('res.partner', string='Transporteur')
    # matricule = fields.Many2one('fleet.vehicle', string='Matricule')
    # ref_transport = fields.Char(string='Réf. Transport')
    # marque = fields.Char(string='Marque', compute='compute_marque')
    #
    # @api.depends('matricule', 'ref_transport')
    # def compute_marque(self):
    #     for rec in self:
    #         rec.marque = False
    #         if rec.matricule and rec.ref_transport:
    #             rec.marque = str(rec.matricule.license_plate) + ' / ' + str(rec.ref_transport)
    #
    #
    # date_voyage = fields.Datetime(string='Date & Heure de voyage')
    # num_connaissement = fields.Char(string='N° Connaissement')
    # poids_brut = fields.Float(string='Poids Brut')
    # nbr_contenant = fields.Float(string='Nbre de contenant')
    # type_contenant = fields.Char(string='Type Contenant')
    # unit_id = fields.Many2one('uom.uom', 'Unité de mesure')
    # nbr_palette = fields.Char(string='Nbre de palette')

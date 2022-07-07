from odoo import models, fields, api, _
import pytz
from datetime import datetime, timedelta
import os
import csv
import base64
import io
import pandas as pd


class DhTransitDossier(models.Model):
    _name = 'dh.transit.dossier'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'num_dossier'

    # entête Du Dossier
    #############################################################

    statut = fields.Selection([('nouveau', 'Nouveau'), ('pret', 'Prêt'),('encours_traitement', 'En cours de traitement'),
                               ('att_confirm', 'Attente de confirmation'), ('encours_dedouanement', 'En cours de Dédouanement'),
                               ('dedouanement_acheve', 'Dédouanement achevé'),
                               ('doc_rem_transporteur', 'Documents remis au transporteur')], string='Statut',
                              tracking=True, default='nouveau')
    progress = fields.Float("Progression", compute='compute_progress_state', store=True)
    priority = fields.Selection(
        [('normal', 'Normal'), ('urgent', 'Urgent')],
        string='Priorité', default='normal', tracking=True)
    parent_id = fields.Many2one('dh.transit.dossier', string='Dossier Parent')
    # attachment_id = fields.Binary("File")
    @api.depends('statut')
    def compute_progress_state(self):
        for rec in self:
            rec.progress = 0
            if rec.statut in ['nouveau', 'pret']:
                rec.progress = 0
            elif rec.statut in ['encours_traitement', 'att_confirm']:
                rec.progress = 25
            elif rec.statut == 'encours_dedouanement':
                rec.progress = 50
            elif rec.statut == 'dedouanement_acheve':
                rec.progress = 75
            elif rec.statut == 'doc_rem_transporteur':
                rec.progress = 100

    type_dossier = fields.Selection([('provisoire', 'Provisoire'), ('definitif', 'Définitif')], string='Type dossier', tracking=True)
    n_dum = fields.Char(string='N° Dum', tracking=True)
    n_serie = fields.Char(string='N° Série', tracking=True)
    n_sous_dum = fields.Char(string='N° Sous Dum', tracking=True)
    date_start_dum = fields.Date(string='Date début Dum', tracking=True)
    date_end_dum = fields.Date(string='Date fin Dum', tracking=True)
    code_regime = fields.Many2one('dh.transit.regime', string='Régime', tracking=True) # Code régime
    description_regime = fields.Char(string='Désignation régime', related='code_regime.description')
    code_bureau_dedouanement = fields.Many2one('dh.transit.bureau', string='Bureau dédouanement', tracking=True) # Code Bureau dédouanement
    description_bureau_dedouanement = fields.Char(string='Désignation bureau dédouanement', related='code_bureau_dedouanement.description')
    code_arrondissement = fields.Many2one('dh.transit.arrondissement', string='Arrondissement', tracking=True) # Code Arrondissement
    description_arrondissement = fields.Char(string='Désignation Arrondissement', related='code_arrondissement.description')
    code_bureau_destination = fields.Many2one('dh.transit.bureau', string='Bureau destination', tracking=True) # Code Bureau destination
    description_bureau_destination = fields.Char(string='Désignation bureau destination', related='code_bureau_destination.description')
    code_lieu_stockage = fields.Many2one('dh.transit.lieu.stockage', string='Lieu stockage', tracking=True) # Code Lieu stockage
    description_lieu_stockage = fields.Many2one('res.partner', string='Désignation lieu stockage', related='code_lieu_stockage.lieu_stockage')
    soumissionnaire = fields.Many2one('res.partner', string='Nom Soumissionnaire', tracking=True)
    client_facturation = fields.Many2one('res.partner', string='Client facturation', tracking=True)
    pta = fields.Selection([('sans', 'Sans'), ('avec', 'Avec')], string='PTA', related='code_arrondissement.pta')
    # # Charges Du Dossier
    # #############################################################
    #
    # date_facture = fields.Date(string='Date de facture', tracking=True)
    # n_facture = fields.Char(string='N° facture', tracking=True)
    # n_service = fields.Char(string='N° service', tracking=True)
    # prestataire = fields.Many2one('res.partner', string='Préstataire', tracking=True)
    # prestation = fields.Char(string='Désignation de prestation', related='prestataire.prestation')
    # prix_unitaire = fields.Float(string='Prix unitaire', tracking=True)
    # quantity = fields.Integer(string='Quantité', tracking=True)
    # amount_total = fields.Float(string='Montant Total', tracking=True)
    # code_devise = fields.Many2one('res.currency', string='Code Devise', tracking=True)
    charge_ids = fields.One2many('dh.transit.charges', 'dossier_id', string='Charges')


    #interface :
    compagnie_maritime = fields.Many2one('res.partner', string='Compagnie Maritime', tracking=True)
    ref_compagnie = fields.Char('Réf. Compagnie', related='compagnie_maritime.reference')
    nbr_colis = fields.Char(string='Nbre colis', tracking=True)
    observation = fields.Char(string='Observation', tracking=True)
    document_ids = fields.Many2many('ir.attachment', string="Documents", tracking=True)

    #Détails Du Dossier
    #############################################################

    num_dossier = fields.Char(string='N° Dossier', tracking=True)
    expediteur = fields.Many2one('res.partner', string='Expéditeur', tracking=True)
    destinataire = fields.Many2one('res.partner', string='Destinataire', tracking=True)
    type_declaration = fields.Selection(
        [('normale', 'Normale'), ('nouvelle', 'Nouvelle provisionnelle'), ('occasionnelle', 'Occasionnelle'),
         ('dum_combinee', 'DUM combinée'), ('dum_anticipee', 'DUM anticipée')], string='Type déclaration', tracking=True)
    type_activite = fields.Selection(
        [('import', 'Import'), ('export', 'Export')], string="Type d'activité", tracking=True, related='code_regime.type')
    article_id = fields.Many2one('product.template', string='Marchandise', tracking=True)
    origine_marchandise = fields.Many2one('res.country', string='Origine marchandise', tracking=True)
    origine_image_url = fields.Char(string="Icon", store=True, related='origine_marchandise.image_url')
    provenance = fields.Many2one('res.country', string='Provenance', tracking=True)
    provenance_image_url = fields.Char(string="Icon", store=True, related='provenance.image_url')
    num_manifeste = fields.Char(string='N° Manifeste', tracking=True)
    mode_transport = fields.Many2one('dh.transit.mode.transport', string='Mode transport', tracking=True)
    is_maritime = fields.Boolean(string='Est maritime?', related='mode_transport.is_maritime')
    type_transport = fields.Many2one('dh.transit.type.transport', string='Type transport', tracking=True)
    date_heure_operation = fields.Datetime(string="Date & Heure prévue de l'opération")

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
    transporteur = fields.Many2one('res.partner', string='Transporteur', tracking=True)
    ref_transporteur = fields.Char(string='Réf Client', tracking=True)
    matricule = fields.Many2one('fleet.vehicle', string='Matricule', tracking=True)
    ref_transport = fields.Char(string='Réf. Transport', tracking=True)
    marque = fields.Char(string='Marque', compute='compute_marque')

    @api.depends('matricule', 'ref_transport')
    def compute_marque(self):
        for rec in self:
            rec.marque = False
            if rec.matricule and rec.ref_transport:
                rec.marque = str(rec.matricule.license_plate) + ' / ' + str(rec.ref_transport)

    date_voyage = fields.Datetime(string='Date & Heure de voyage', tracking=True)
    num_connaissement = fields.Char(string='N° Connaissement', tracking=True)
    poids_brut = fields.Float(string='Poids Brut', tracking=True)
    nbr_contenant = fields.Float(string='Nbre de contenant', tracking=True)
    type_contenant = fields.Char(string='Type Contenant', tracking=True)
    unit_id = fields.Many2one('uom.uom', 'Unité mesure', tracking=True)
    nbr_palette = fields.Char(string='Nbre palette', tracking=True)

    #############################################################
    # Info complémentaires - Dossier
    is_tr = fields.Boolean(string='TR ?', tracking=True)
    num_tr = fields.Integer(string='TR', tracking=True)
    date_tr = fields.Datetime(string='Date & Heure TR', tracking=True)
    bureau_concerne = fields.Many2one('dh.transit.bureau', string='Bureau concerné', tracking=True)
    ref_tr = fields.Char(string='Réf TR', tracking=True)
    is_scelle_douane = fields.Boolean(string='Est scelle douane?', tracking=True)
    num_scelle_douane = fields.Char(string='N° scellés Douane', tracking=True)
    is_scelle_client = fields.Boolean(string='Est scelle client?', tracking=True)
    num_scelle_client = fields.Char(string='N° scellés Client', tracking=True)
    pince = fields.Char(string='Pince', tracking=True)
    commentaire = fields.Char(sring='Commentaire', tracking=True)

    #############################################################
    # info complémentaires - Taxation (Achat)

    sens_taxation = fields.Selection(
        [('import', 'Import'), ('export', 'Export')], string='Sens', tracking=True)
    terminal_id = fields.Many2one('dh.transit.terminal', string='Terminal', tracking=True)
    type_unite = fields.Many2one('dh.transit.unite', string="Type d'unité", tracking=True)
    type_sous_unite = fields.Many2one('dh.transit.sous.unite', string="Sous type d'unité",  domain=lambda self: [('type_unite', '=', self.type_unite.id)], tracking=True)
    n_unite = fields.Char(string='N° Unité')
    n_tracteur = fields.Char(string='N° Tracteur')
    n_plateau = fields.Char(string='N° Plateau')
    nature = fields.Selection(
        [('vide', 'Vide'), ('plein', 'Plein')], string='Nature', tracking=True)

    #############################################################
    # Documents annexés
    docs_annexe_ids = fields.One2many('dh.transit.docs', 'dossier_id', string='Documents annexés')

    #############################################################
    # Liste des factures
    dh_transit_facture_ids = fields.One2many('dh.transit.facture', 'transit_dossier_id')

    #############################################################
    # Circuit validation
    dh_transit_circuit_validation_ids = fields.One2many('dh.transit.circuit.validation', 'dh_transit_dossier_id')
    annexe_disable_auto = fields.Boolean(string='Déactivé annexations automatique?', default=False)
    charges_disable_auto = fields.Boolean(string='Déactivé charges automatique?', default=False)

    @api.onchange('type_activite', 'code_bureau_dedouanement', 'mode_transport', 'type_transport', 'code_regime', 'code_bureau_destination') # , 'docs_annexe_ids'
    def regenerer_ligne_annexation(self):
        for rec in self:
            if rec.annexe_disable_auto == False:
                lines = []
                today_utc = pytz.UTC.localize(datetime.now())
                if self.env.user.tz:
                    tz = self.env.user.tz
                else:
                    tz = 'UTC'
                today_tz = today_utc.astimezone(pytz.timezone(tz))
                now = datetime.now() + timedelta(hours=int(str(today_tz)[-4]))
                if rec.type_activite and rec.code_bureau_dedouanement.id and rec.mode_transport.id and rec.type_transport.id and rec.code_regime.id and rec.code_bureau_destination.id:
                    annexation = self.env['dh.transit.parametre.annexation'].search(
                        [('type_operation', '=', rec.type_activite),
                         ('code_bureau_dedouanement', '=', rec.code_bureau_dedouanement.id),
                         ('mode_transport', '=', rec.mode_transport.id), ('type_transport', '=', rec.type_transport.id),
                         ('code_regime', '=', rec.code_regime.id),
                         ('code_bureau_destination', '=', rec.code_bureau_destination.id)], limit=1)
                    if len(annexation) > 0 and len(rec.docs_annexe_ids) == 0:
                        for line_annexe in annexation.annexation_lines:
                            line = {'type_annexation': line_annexe.type.id,
                                    'dossier_id': rec.id,
                                    'date_annexation': now.strftime('%Y-%m-%d'),
                                    'heure_annexation': now.time().hour + now.time().minute / 60.0}
                            lines.append(line)
                        if len(lines) > 0:
                            rec.docs_annexe_ids = [(0, 0, x) for x in lines]

                    elif len(annexation) > 0 and len(rec.docs_annexe_ids) != 0:
                        if annexation.annexation_lines.mapped('type') not in rec.docs_annexe_ids.mapped('type_annexation'):
                            for line_annexe in annexation.annexation_lines:
                                if line_annexe.type not in rec.docs_annexe_ids.mapped('type_annexation'):
                                    line = {'type_annexation': line_annexe.type.id,
                                            'dossier_id': rec.id,
                                            'date_annexation': now.strftime('%Y-%m-%d'),
                                            'heure_annexation': now.time().hour + now.time().minute / 60.0}
                                    lines.append(line)
                            if len(lines) > 0:
                                rec.docs_annexe_ids = [(0, 0, x) for x in lines]

    @api.onchange('type_declaration', 'code_bureau_dedouanement', 'code_regime', 'code_bureau_destination', 'client_facturation')  # , 'charge_ids'
    def regenerer_ligne_charges(self):
        for rec in self:
            if rec.charges_disable_auto == False:
                lines = []
                today_utc = pytz.UTC.localize(datetime.now())
                if self.env.user.tz:
                    tz = self.env.user.tz
                else:
                    tz = 'UTC'
                today_tz = today_utc.astimezone(pytz.timezone(tz))
                now = datetime.now() + timedelta(hours=int(str(today_tz)[-4]))
                if rec.type_declaration and rec.code_bureau_dedouanement.id and rec.code_regime.id and rec.code_bureau_destination.id and rec.client_facturation.id:
                    charge_standard = self.env['dh.transit.parametres.charges'].search(
                        [('type_declaration', '=', rec.type_declaration),
                         ('code_bureau_dedouanement', '=', rec.code_bureau_dedouanement.id),
                         ('code_regime', '=', rec.code_regime.id),
                         ('code_bureau_destination', '=', rec.code_bureau_destination.id)], limit=1)
                    charge_client = self.env['dh.transit.parametres.charges'].search(
                        [('type_declaration', '=', rec.type_declaration),
                         ('code_bureau_dedouanement', '=', rec.code_bureau_dedouanement.id),
                         ('code_regime', '=', rec.code_regime.id),
                         ('code_bureau_destination', '=', rec.code_bureau_destination.id),
                         ('client_id', '=', rec.client_facturation.id)], limit=1)

                    charge = charge_client if len(charge_client) > 0 else charge_standard

                    if len(charge) > 0 and len(rec.charge_ids) == 0:
                        for line_charge in charge.parametres_charges_line_ids:
                            line = {'product_id': line_charge.product_id.id,
                                    'prix_unitaire': line_charge.prix,
                                    'quantity': 1,
                                    'confirmation_client': True,
                                    'dossier_id': rec.id,
                                    'date_piece': now.strftime('%Y-%m-%d')}
                            lines.append(line)
                        if len(lines) > 0:
                            rec.charge_ids = [(0, 0, x) for x in lines]

                    elif len(charge) > 0 and len(rec.charge_ids) != 0:
                        if charge.parametres_charges_line_ids.mapped('product_id') not in rec.charge_ids.mapped('product_id'):
                            for line_charge in charge.parametres_charges_line_ids:
                                if line_charge.product_id not in rec.charge_ids.mapped('product_id'):
                                    line = {'product_id': line_charge.product_id.id,
                                            'prix_unitaire': line_charge.prix,
                                            'quantity': 1,
                                            'confirmation_client': True,
                                            'dossier_id': rec.id,
                                            'date_piece': now.strftime('%Y-%m-%d')}
                                    lines.append(line)
                            if len(lines) > 0:
                                rec.charge_ids = [(0, 0, x) for x in lines]

                    products_sup = []
                    charge_line_email = []
                    createur = False
                    if len(rec.charge_ids) != 0 and len(charge_client) > 0 and rec.statut != 'att_confirm':
                        for line_charge in rec.charge_ids:
                            if line_charge.product_id not in charge_client.parametres_charges_line_ids.mapped('product_id') and line_charge.confirmation_client == False:

                                createur = line_charge.create_uid
                                products_sup.append(line_charge.product_id)
                                charge_line_email.append(line_charge)
                                rec.statut = 'att_confirm'

                        if len(charge_line_email) > 0:

                            rec.button_envoye_message(charge_line_email, createur)
                            #sent mail

    def button_envoye_message(self, charge_line_email, Creator):
        template_id = self.env.ref('dh_transit.mail_transit_dossier')  # xml id of your email template
        email_list=[]

        if self.client_facturation.email!=False:
            email_list.append(self.client_facturation.email)

            for email in email_list:
                template_id.email_to = email
                template_id.reply_to = email
                template_id.email_from = 'admin'
                email_values = {'key_transit_dossier': charge_line_email,'Creator_user':Creator}
                template_id.with_context(email_values).sudo().send_mail(self.id, force_send=True)

    def button_confirmation_client(self):
        for rec in self:
            for line in rec.charge_ids.filtered(lambda x:x.confirmation_client == False):
                line.write({'confirmation_client': True})
            rec.statut = 'encours_traitement'

    @api.model
    def create(self, vals):
        vals['num_dossier'] = self.env['ir.sequence'].next_by_code('dh.transit.dossier')
        vals['statut']='pret'
        res = super().create(vals)
        res.regenerer_ligne_annexation()
        res.regenerer_ligne_charges()

        #crée reportoires
        parent_dir = self.env['ir.config_parameter'].sudo().get_param(
                                'dh_transit.path_puerto')
        directory = res.num_dossier
        path_parent = os.path.join(parent_dir, directory)
        os.mkdir(path_parent)

        for type_annexe in self.env['dh.transit.type.annexation'].search([]):
            parent_dir = path_parent.replace(' ', '_')
            directory = type_annexe.docs_annexe.replace(' ', '_')
            path = os.path.join(parent_dir, directory)
            os.mkdir(path)

        return res

    def write(self, vals):
        res = super().write(vals)
        self.regenerer_ligne_annexation()
        self.regenerer_ligne_charges()
        return res

    def button_encours_dedouanement(self):
        for rec in self:
            rec.statut='encours_dedouanement'

    def button_dedouanement_acheve(self):
        for rec in self:
            rec.statut='dedouanement_acheve'

    def button_doc_rem_transporteur(self):
        for rec in self:
            rec.statut = 'doc_rem_transporteur'


    # def execute(self):
    #     file = base64.b64decode(self.attachment_id)
    #     toread = io.BytesIO()
    #     toread.write(file)  # pass your `decrypted` string as the argument here
    #     toread.seek(0)  # reset the pointer
    #     df = pd.read_excel(toread)
    #     for r in df.index:
    #         print('df', df["no_facture"][r])
    #         print('test', df["test"][r])
    #         self.env['dh.transit.facture'].create({'transit_dossier_id': self.env['dh.transit.dossier'].search([('num_dossier', '=', df["num_dossier"][r])]).id, 'n_facture': df["no_facture"][r]})


    def action_importer_facture(self):
        transfert = self.env['wizard.dh.importer.facture'].create({
            'dossier_id': self.id,
        })
        return {
            'name': 'Importer Facture',
            'res_model': 'wizard.dh.importer.facture',
            'view_type': 'form',
            'view_mode': 'form',
            'res_id': transfert.id,
            'type': 'ir.actions.act_window',
            'target': 'new'
        }

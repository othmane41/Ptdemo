from odoo import models, fields, api,_
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError
import base64
import io
import pandas as pd

class DhImporterFacture(models.Model):
    _name = "wizard.dh.importer.facture"

    attachment_id = fields.Binary("Fichier")
    dossier_id=fields.Many2one('dh.transit.dossier', string='N° dossier')

    def execute(self):
        if self.attachment_id!=False:
            file = base64.b64decode(self.attachment_id)
            toread = io.BytesIO()
            toread.write(file)  # pass your `decrypted` string as the argument here
            toread.seek(0)  # reset the pointer
            df = pd.read_excel(toread)
            for r in df.index:

                if type(df["Producteur"][r]) != float:
                    facture_id = self.env['dh.transit.facture'].create({'transit_dossier_id': self.dossier_id.id,'producteur_id': self.env['res.partner'].search([('name', '=', df["Producteur"][r])]).id,'station_id':self.env['dh.station'].search([('display_name', '=', df["numero_station"][r])]).id,'date_facture':df["Date_facture"][r],'n_facture': df["no_facture"][r],'contenant_id':self.env['dh.contenant'].search([('display_name', '=', df["Nbre_contenant"][r])]).id,'fournisseur_id':self.env['res.partner'].search([('name', '=', df["Expediteur"][r])]).id,'destinatire_id':self.env['res.partner'].search([('name', '=', df["Destinataire"][r])]).id,'total_facture':df["Total_facture"][r],'code_devise':self.env['res.currency'].search([('name', '=', df["Devise"][r])]).id,'rate':df["Cours_de_change"][r],'incoterm':self.env['account.incoterms'].search([('name', '=', df["Incoterm"][r])]).id,'rate':df["Cours_de_change"][r],'mode_paiement': self.env['dh.transit.mode.paiement'].search([('mode_paiment', '=', df["Mode_de_paiement"][r])]).id,'poids_brut_total':df["Poids_Brut_Total"][r],'poids_net_total':df["Poids_Net_Total"][r]})
                    if type(df["facture/Code_NGP"][r]) != float:
                        self.env['dh.transite.facture.lines'].create(
                            {'dh_transit_facture_id': facture_id.id,
                             'code_ngp':df["facture/Code_NGP"][r],
                             'code_article_expediteur': df["facture/code_article_expediteur"][r],
                             'code_article_destinataire': df["facture/code_article_destinatire"][r],
                             'designation_commerciale': df["facture/designation_commerciale"][r],
                             'unite_mesure':self.env['dh.transit.uom'].search([('code_unite', '=', df["facture/unite_mesure"][r])]).id,
                              'quantite':df["facture/quantite"][r],
                              'poids_net':df["facture/poids_net"][r],
                             'valeur':df["facture/valeur"][r],
                             'code_pays_id':self.env['res.country'].search([('name', '=', df["facture/unite_mesure"][r])]).id,



                             })
                else:
                    if type(df["facture/Code_NGP"][r]) != float:
                        self.env['dh.transite.facture.lines'].create(
                            {'dh_transit_facture_id': facture_id.id,
                             'code_ngp':df["facture/Code_NGP"][r],
                             'code_article_expediteur': df["facture/code_article_expediteur"][r],
                             'code_article_destinataire': df["facture/code_article_destinatire"][r],
                             'designation_commerciale': df["facture/designation_commerciale"][r],
                             'unite_mesure':self.env['dh.transit.uom'].search([('code_unite', '=', df["facture/unite_mesure"][r])]).id,
                              'quantite':df["facture/quantite"][r],
                              'poids_net':df["facture/poids_net"][r],
                             'valeur':df["facture/valeur"][r],
                             'code_pays_id':self.env['res.country'].search([('name', '=', df["facture/unite_mesure"][r])]).id,



                             })

        self.attachment_id=False


from odoo import models, fields, api

class DhTransitTypeAnnexation(models.Model):
    _name = 'dh.transit.type.annexation'
    _rec_name = "docs_annexe"

    docs_annexe = fields.Char(string='Documents annexé')
    type_badr = fields.Selection(
        [('auto_douane', 'Autorisations de la Douane'), ('demande_consig', 'Demande de consignation valeur'),
         ('demande_arbit', "Demande d'arbitrage valeur"), ('autre_auto_admin', "Autres autorisations administratives"),
         ('docs_commerce', "Documents commerciaux"), ('titre_prop_trans', "Titre de propriété et / ou de Transport")],
        string='Type Sustéme Badr')
    type_puerto = fields.Selection(
        [('outlook', 'Outlook'), ('docs_commerce', 'Documents Commerciaux'),
         ('portail', "Portails"), ('certificats', "Certificats"),
         ('docs_finance', "Documents financiers")], string='Type Puerto Transit')

    format_annexe = fields.Selection(
        [('email', 'Email'), ('pdf_excel', 'Document PDF ou Excel'),
         ('pdf', "Document PDF"), ('excel', "Fichier Excel")], string='Format')
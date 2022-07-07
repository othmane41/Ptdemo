# -*- coding: utf-8 -*-
{
    'name': "Dynamic puerto transit",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Dynamic Horizon : Errzieq El Mehdi",
    'website': "http://www.dynamichorizon.ma",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'fleet', 'sale', 'hr', 'hr_recruitment', 'mail', 'crm', 'contacts', 'sales_team'],

    # always loaded
    'data': [
        'data/ir_sequence_data.xml',
        'security/ir.model.access.csv',
        'views/dh_transit_dossier.xml',
        'views/res_country.xml',
        'views/res_partner.xml',
        'views/dh_transit_regime.xml',
        'views/dh_transit_arrondissement.xml',
        'views/dh_transit_bureau.xml',
        'views/dh_transit_lieustockage.xml',
        'views/dh_transit_mode_transport.xml',
        'views/dh_transit_type_transport.xml',
        'views/dh_transit_type_annexation.xml',
        'views/dh_transit_mode_paiement.xml',
        'views/dh_transit_uom.xml',
        'views/dh_transit_terminal.xml',
        'views/dh_transit_unite.xml',
        'views/dh_transit_department.xml',
        'views/dh_transit_priorite.xml',
        'views/dh_type_interlocuteur.xml',
        'views/res_city.xml',
        'views/dh_etat_tasks.xml',
        'views/dh_puerto_settings.xml',
        'views/dh_transit_parametres_charges.xml',
        'views/dh_station.xml',
        'views/dh_contenant.xml',
        'views/dh_mail_confirmation_article.xml',
        'views/dh_transit_parametre_annexation.xml',
        'views/dh_mail_confirmation_article.xml',
        'views/dh_transit_parametres_charges_line.xml',
        'views/dh_wizard_transit_dossier.xml',
        'views/dh_wizard_importer_facture.xml',
        'views/dh_product_category.xml',
        'views/dh_menus.xml',
    ],

    'assets': {
        'web.assets_backend': [
            'dh_transit/static/src/css/cps.less',
        ],
    },
}

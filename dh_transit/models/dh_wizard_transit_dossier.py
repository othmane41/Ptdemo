from odoo import models, fields, api

class DhWizardTransitDossier(models.Model):
    _name = 'dh.wizard.transit.dossier'

    dossier_parent_id = fields.Many2one('dh.transit.dossier', string='Dossier Parent')

    def write_transit_dossier(self):
         for rec in self.env['dh.transit.dossier'].browse(self._context.get('active_ids', [])):
                 rec.write({'parent_id': self.dossier_parent_id})




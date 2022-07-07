from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import shutil
import os
import base64

class DhTransitDocs(models.Model):
    _name = 'dh.transit.docs'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'date_annexation'

    date_annexation = fields.Date(string="Date d'annexation")
    heure_annexation = fields.Float(string="Heure d'annexation")
    type_annexation = fields.Many2one('dh.transit.type.annexation', string="Type d'annexe")
    nom_doc_annexe = fields.Char(string="Documents annexé", related='type_annexation.docs_annexe')
    attachment_ids = fields.Many2many('ir.attachment', string='Piéces jointes', track_visibility='always')
    commentaire = fields.Char(string='Commentaire')
    dossier_id = fields.Many2one('dh.transit.dossier', string='N° dossier')
    url = fields.Char('URL')
    worksheet_type = fields.Selection([
        ('pdf', 'PDF'), ('google_slide', 'Google Slide')],
        string="feuille de travail", default="pdf",
        help="Définit si vous souhaitez utiliser un PDF ou une diapositive Google comme feuille de travail."
    )
    worksheet = fields.Binary(string='file', attachment=True)
    worksheet_google_slide = fields.Char('diapositive Google',
                                         help="Collez l'URL de votre diapositive Google. Assurez-vous que l'accès au document est public.")

    charge_id = fields.Many2one('dh.transit.charges', track_visibility='always')
    charge_line_id = fields.Many2one('dh.transit.charges.lines', track_visibility='always')

    # @api.constrains("attachment_ids")
    # def _check_auto_exclusion(self):
    #     for rec in self:
    #         if len(rec.attachment_ids) > 1:
    #             raise ValidationError(
    #                 _(
    #                     "Vous pouvez glissé un seul fichier par ligne"
    #                 )
    #             )

    def button_url(self):
        return {
            'type': 'ir.actions.act_url',
            'target': 'new',
            'url' : '%s' % (self.url)
        }

    # @api.onchange('attachment_ids')
    def compute_url(self):
        for rec in self:
            rec.url = ''
            if len(rec.attachment_ids) > 0:
                for attachment in rec.attachment_ids:
                    f = open(os.path.join(self.env['ir.config_parameter'].sudo().get_param(
                                'dh_transit.path_puerto') + '/' + str(
                        rec.dossier_id.num_dossier).replace(' ', '_') + '/' + str(rec.type_annexation.docs_annexe).replace(
                        ' ', '_'), attachment.name.replace(' ', '_')), 'w+b')
                    f.write(base64.decodestring(attachment.datas))
                    f.close()

                    os.rename(r'%s' % (self.env['ir.config_parameter'].sudo().get_param(
                                'dh_transit.path_puerto') + '/' + str(
                        rec.dossier_id.num_dossier).replace(' ', '_') + '/' + str(
                        rec.type_annexation.docs_annexe).replace(' ', '_') + '/' + attachment.name.replace(' ',
                                                                                                                      '_')),
                              r'%s' % (self.env['ir.config_parameter'].sudo().get_param(
                                'dh_transit.path_puerto') + '/' + str(
                                  rec.dossier_id.num_dossier).replace(' ', '_') + '/' + str(
                                  rec.type_annexation.docs_annexe).replace(' ', '_') + '/' + str(
                                  rec.dossier_id.num_dossier).replace(' ', '_') + '-' + str(
                                  rec.type_annexation.docs_annexe).replace(' ', '_').replace(' ', '_') + '-' +
                                       attachment.name.replace(' ', '_')))

                url = ''
                for attachment in rec.attachment_ids:
                     url += '<a href="file://%s/%s">%s</a><br/>' % (self.env['ir.config_parameter'].sudo().get_param(
                                'dh_transit.path_puerto') + '/' + str(
                        rec.dossier_id.num_dossier).replace(' ', '_') + '/' + str(
                        rec.type_annexation.docs_annexe).replace(' ', '_'), str(rec.dossier_id.num_dossier).replace(
                        ' ', '_') + '-' + str(
                        rec.type_annexation.docs_annexe).replace(' ', '_').replace(' ', '_') + '-' + attachment.name.replace(' ', '_'),
                                                                 str(attachment.name))

                rec.url = url
                rec.attachment_ids.unlink()

    def create(self, vals):
        res = super().create(vals)
        if type(vals) == list:
            for val in vals:
                if 'attachment_ids' in val:
                    if len(val['attachment_ids']) > 0:
                        res.compute_url()
        else:
            if 'attachment_ids' in vals:
                if len(vals['attachment_ids']) > 0:
                    res.compute_url()
        return res

    def write(self, vals):
        res = super().write(vals)
        if type(vals) == list:
            for val in vals:
                if 'attachment_ids' in val:
                    if len(val['attachment_ids']) > 0:
                        self.compute_url()
        else:
            if 'attachment_ids' in vals:
                if len(vals['attachment_ids']) > 0:
                    self.compute_url()
        return res




    def delete_doc(self):
        for rec in self:
            rec.charge_id.unlink()
            rec.charge_line_id.unlink()
            rec.unlink()


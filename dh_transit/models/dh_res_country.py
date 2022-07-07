from odoo import models, fields, api


class DhResCountry(models.Model):
    _inherit = 'res.country'

    iso_alpha_2 = fields.Char(string='ISO 3166-1 alpha-2')
    iso_alpha_3 = fields.Char(string='ISO 3166-1 alpha-3')
    iso_alpha_numerique = fields.Char(string='ISO 3166-1 numérique')
    ville_ids= fields.One2many('res.city','dh_country_id')


    def name_get(self):
        ret_list = []
        for record in self:
            if record.iso_alpha_2:
                name = '%s - %s' % (record.iso_alpha_2, record.name)
            elif record.iso_alpha_3:
                name = '%s - %s' % (record.iso_alpha_3, record.name)
            elif record.iso_alpha_numerique:
                name = '%s - %s' % (record.iso_alpha_numerique, record.name)
            else:
                name = record.name
            ret_list.append((record.id, name))
        return ret_list

    display_name = fields.Char("Display Name", compute="_compute_display_name")

    @api.depends('name', 'iso_alpha_2', 'iso_alpha_3', 'iso_alpha_numerique')
    def _compute_display_name(self):
        for rec in self:
            if rec.iso_alpha_2:
                rec.display_name = '%s - %s' % (rec.iso_alpha_2, rec.name)
            elif rec.iso_alpha_3:
                rec.display_name = '%s - %s' % (rec.iso_alpha_3, rec.name)
            elif rec.iso_alpha_numerique:
                rec.display_name = '%s - %s' % (rec.iso_alpha_numerique, rec.name)
            else:
                rec.display_name = rec.name
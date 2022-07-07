from odoo import models, fields, api


class DhTransitArrondissement(models.Model):
    _name = 'dh.transit.arrondissement'

    code = fields.Char(string='Code', required=True)
    description = fields.Char(string='Description')
    pta = fields.Selection([('sans', 'Sans'), ('avec', 'Avec')], string='PTA', default='sans')

    @api.depends("code", "description")
    def name_get(self):
        result = []
        for rec in self:
            if rec.code and rec.description:
                name = " - ".join([rec.code, rec.description])
            elif rec.code and not rec.description:
                name = rec.code
            else:
                name = False
            result.append((rec.id, name))
        return result
from odoo import models, fields, api


class DhTransitBureau(models.Model):
    _name = 'dh.transit.bureau'

    code = fields.Char(string='Code', required=True)
    description = fields.Char(string='Description')

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

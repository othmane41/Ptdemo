from odoo import models, fields, api


class DhTransitRegime(models.Model):
    _name = 'dh.transit.regime'

    code = fields.Char(string='Code', required=True)
    description = fields.Char(string='Description')
    type = fields.Selection(
        [('import', 'Import'), ('export', 'Export')], string="Type", default='import')

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
from odoo import models, fields, api


class DhTransitLieuStockage(models.Model):
    _name = 'dh.transit.lieu.stockage'

    code_bureau = fields.Many2one('dh.transit.bureau', string='Code Bureau')
    description_bureau = fields.Char(string='Bureau', related='code_bureau.description')
    code_stockage = fields.Char(string='Code lieu de stockage', required=True)
    lieu_stockage = fields.Many2one('res.partner', string='Lieu de stockage')

    @api.depends("code_stockage", "lieu_stockage")
    def name_get(self):
        result = []
        for rec in self:
            if rec.code_stockage and rec.lieu_stockage:
                name = " - ".join([rec.code_stockage, rec.lieu_stockage.name])
            elif rec.code_stockage and not rec.lieu_stockage:
                name = rec.code_stockage
            else:
                name = False
            result.append((rec.id, name))
        return result
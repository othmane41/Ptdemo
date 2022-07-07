# -*- coding: utf-8 -*-
from odoo import models, fields, api,  _
from ast import literal_eval


class PuertoSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    path_puerto = fields.Char(string='Path files')

    def set_values(self):
        res = super(PuertoSettings, self).set_values()
        self.env['ir.config_parameter'].set_param('dh_transit.path_puerto',
                                                  self.path_puerto)
        return res

    @api.model
    def get_values(self):
        res = super(PuertoSettings, self).get_values()
        res.update(
            path_puerto=self.env['ir.config_parameter'].sudo().get_param('dh_transit.path_puerto'))
        return res

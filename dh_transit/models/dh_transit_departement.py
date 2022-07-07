from odoo import models, fields, api


class Dhdepartement(models.Model):
    _inherit = 'hr.department'
    name = fields.Char('Service', required=True)
    parent_id = fields.Many2one('hr.department', string='Departement', index=True, domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")
    mail_activity_type_ids = fields.Many2many('mail.activity.type', string="Tâches", tracking=True)



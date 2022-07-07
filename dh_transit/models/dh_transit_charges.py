from odoo import models, fields, api
from datetime import datetime, timedelta,date
import pytz
from pytz import timezone, UTC

class DhTransitCharges(models.Model):
    _name = 'dh.transit.charges'

    date_piece = fields.Date(string='Date de piéce', tracking=True)
    n_piece = fields.Char(string='N° piéce', tracking=True)
    n_service = fields.Char(string='N° service', tracking=True)
    prestataire = fields.Many2one('res.partner', string='Préstataire', tracking=True)
    prestation = fields.Char(string='Désignation de prestation', related='prestataire.prestation')
    product_id = fields.Many2one('product.product', string='Article')
    prix_unitaire = fields.Float(string='Prix unitaire', tracking=True)
    quantity = fields.Integer(string='Quantité', tracking=True)
    amount_total = fields.Float(string='Montant Total', compute='compute_total', tracking=True)
    code_devise = fields.Many2one('res.currency', string='Code Devise', tracking=True)
    dossier_id = fields.Many2one('dh.transit.dossier', string='N° dossier')
    confirmation_client = fields.Boolean(string='Confirme client', default=False)
    dh_transit_docs_id=fields.Many2one('dh.transit.docs')
    line_ids = fields.One2many('dh.transit.charges.lines', 'charge_id', string='Lignes')
    est_charge_client = fields.Boolean(string='Est charge client?', related='product_id.categ_id.est_charge_client')

    @api.onchange('line_ids')
    def onchange_lines(self):
        for rec in self:
            if len(rec.line_ids) > 0:
                rec.prix_unitaire = sum(rec.line_ids.mapped('prix_unitaire')) / len(rec.line_ids)
                rec.quantity = sum(rec.line_ids.mapped('quantity'))

    @api.depends('prix_unitaire', 'quantity')
    def compute_total(self):
        for rec in self:
            if len(rec.line_ids) == 0:
                rec.amount_total = rec.prix_unitaire * rec.quantity
            else:
                rec.amount_total = sum(rec.line_ids.mapped('amount_total'))

    def write(self, vals):
        if 'n_piece' in vals:
            if vals['n_piece'] != False and self.n_piece == False:
                today_utc = pytz.UTC.localize(datetime.now())
                if self.env.user.tz:
                    tz = self.env.user.tz
                else:
                    tz = 'UTC'
                today_tz = today_utc.astimezone(pytz.timezone(tz))
                now = datetime.now() + timedelta(hours=int(str(today_tz)[-4]))

                docs_line=self.env['dh.transit.docs'].create({
                    'date_annexation': date.today(),
                    'heure_annexation': now.time().hour + now.time().minute / 60.0,
                    'dossier_id': self.dossier_id.id,

                })

                vals['dh_transit_docs_id']=docs_line.id

        res = super().write(vals)

        print("test",self.dh_transit_docs_id)
        return res

    @api.model
    def create(self, vals):
        res = super().create(vals)
        if 'n_piece' in vals:
            if vals['n_piece'] != False:
                today_utc = pytz.UTC.localize(datetime.now())
                if self.env.user.tz:
                    tz = self.env.user.tz
                else:
                    tz = 'UTC'
                today_tz = today_utc.astimezone(pytz.timezone(tz))
                now = datetime.now() + timedelta(hours=int(str(today_tz)[-4]))
                docs_line = self.env['dh.transit.docs'].create({
                    'date_annexation': date.today(),
                    'heure_annexation': now.time().hour + now.time().minute / 60.0,
                    'dossier_id':res.dossier_id.id,
                    'charge_id':res.id,
                     })
                res.write({'dh_transit_docs_id': docs_line.id})
                print("test",docs_line.charge_id)
        return res



    def delete_charge(self):
        for rec in self:
            rec.dh_transit_docs_id.unlink()
            rec.line_ids.delete_charge_line()
            rec.unlink()


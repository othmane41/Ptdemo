from odoo import models, fields, api
from datetime import datetime, timedelta,date
import pytz

class DhTransitChargesLines(models.Model):
    _name = 'dh.transit.charges.lines'

    charge_id = fields.Many2one('dh.transit.charges', string='Charge')
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
    dossier_id = fields.Many2one('dh.transit.dossier', string='N° dossier', related='charge_id.dossier_id',store=True)
    confirmation_client = fields.Boolean(string='Confirme client', default=False)
    est_charge_client = fields.Boolean(string='Est charge client?', related='product_id.categ_id.est_charge_client')
    dh_transit_docs_id = fields.Many2one('dh.transit.docs')

    @api.depends('prix_unitaire', 'quantity')
    def compute_total(self):
        for rec in self:
            rec.amount_total = rec.prix_unitaire * rec.quantity

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
                    'charge_line_id':res.id,

                     })
                res.write({'dh_transit_docs_id': docs_line.id})
        return res



    def delete_charge_line(self):
        for rec in self:
            rec.dh_transit_docs_id.unlink()
            rec.unlink()


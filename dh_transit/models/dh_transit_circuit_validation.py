from odoo import models, fields, api


class DhTransitCircuitValidation(models.Model):
    _name = 'dh.transit.circuit.validation'
    # _rec_name = 'display_name'

    department_id= fields.Many2one('hr.department','Département')
    tache_id = fields.Many2one('', string='Service affecté')
    utilisateur_affcter_id=fields.Many2one('res.users','Utilisateur Affecté')
    intitule_tache_ids = fields.Many2one('mail.activity.type', string="Intitulé de tâche")
    priorite_id=fields.Many2one('dh.transit.priorite','Priorité')
    date_affectation = fields.Date(string="Date d'affectation", tracking=True)
    heure_affectation=fields.Float("Heure d'affectation",tracking=True)
    createur_tache_id=fields.Many2one('res.users','Créateur de tâche')
    etape_encours=fields.Selection([('preAlerte', 'Pré-alerte'), ('enCoursTraitement', 'En cours de traitement'),('EnCoursDédouanement', 'En cours de Dédouanement'),('DédouanementAchevé', 'Dédouanement Achevé')], string='Etape Encours', tracking=True)
    etat_tache= fields.Many2one('dh.etat.tasks', string='Etat de la tâche', tracking=True)
    commentaire= fields.Char(string='Commentaire', tracking=True)
    dh_transit_dossier_id=fields.Many2one('dh.transit.dossier')










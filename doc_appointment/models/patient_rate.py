from odoo import fields , models , api , _

class PatientRate(models.Model):
    _name = 'patient.rate'
    _inherit = ['mail.thread' , 'mail.activity.mixin']
    _rec_name = 'seq'

    seq = fields.Char(string='clinic sequence' , readonlt=True,default="New")

    service_id = fields.Many2one('appointment.type')

    user_id = fields.Many2one('res.partner')

    appointment_id = fields.Many2one('appointment.type')



    rating = fields.Selection([('1', '1'), ('2', '2') , ('3', '3') , ('4', '4') , ('5', '5') ],
                     string=' Rating', default='1', required=True)

    desc = fields.Text(string='description')

    @api.model
    def create(self, vals):
        vals['seq'] = self.env['ir.sequence'].next_by_code('patient.rate') or _("New")
        return super().create(vals)


from datetime import date
from odoo import api , fields , models
from dateutil import relativedelta

class HospitalPatient(models.Model):
    _name = "hospital.patient"
    _inherit = ['mail.thread' , 'mail.activity.mixin']
    _description = "Hospital Patient"
    _order='id desc'

    name = fields.Char(string='Name' , tracking =True , )
    date_of_birth = fields.Date(string='Date of birth')
    ref = fields.Char(string="Reference", tracking =True , default='odoo mates' )
    age = fields.Integer(string='Age', compute='_compute_age' ,inverse='_inverse_computed_age' , tracking =True , store=True)
    gender = fields.Selection([('male','Male'),('female','Female')],string='Gender', tracking =True)
    active = fields.Boolean(string="Active" , default='true', tracking =True)
    appointment_id = fields.Many2one('hospital.appointment', string='Appointment')
    image = fields.Image(string="image")
    tag_ids = fields.Many2many('patient.tag' , string="tags")
    appointment_time = fields.Integer(string='App_time')
    is_birthday = fields.Boolean(compute = '_compute_is_birthdate')
    phone = fields.Char()
    email = fields.Char()
    website = fields.Char()
    sequence = fields.Char()


    @api.depends('date_of_birth')
    def _compute_is_birthdate(self):
        for rec in self:
            is_birthday = False
            if rec.date_of_birth:
                today = date.today()
                if today.day == rec.date_of_birth.day and today.month == rec.date_of_birth.month:
                    is_birthday = True
            rec.is_birthday = is_birthday

    @api.depends('age')
    def _inverse_computed_age(self):
        today = date.today()
        for rec in self:
            rec.date_of_birth = today - relativedelta.relativedelta(years = rec.age)

    @api.depends('date_of_birth')
    def _compute_age(self):
        for rec in self:
            today = date.today()
            if rec.date_of_birth:
                rec.age = today.year - rec.date_of_birth.year
            else:
                rec.age = 0

    @api.model
    def create(self , vals):
        vals['sequence'] = self.env['ir.sequence'].next_by_code('hospital.patient')
        return super().create(vals)
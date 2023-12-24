import random
from odoo import api, fields, models
from odoo.exceptions import UserError


class HospitalAppointment(models.Model):
    _name = "hospital.appointment"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Hospital appointment"
    _rec_name = "patient_id"

    patient_id = fields.Many2one('hospital.patient', string='Patient' , ondelete='restrict') #ondelete='cascade'
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string='Gender', tracking=True, related ='patient_id.gender' , readonly=False)
    appointment_time = fields.Datetime(string='Appointment time' , default=fields.Datetime.now)
    booking_date = fields.Date(string='Booking date' , default=fields.Date.context_today)
    ref = fields.Char(string="Reference", tracking =True, help="reference from patient record")
    prescription = fields.Html(string="prescription")
    priority=fields.Selection([
        ('0' ,'normal'),
        ('1' , 'low') ,
        ('2' , 'high') ,
        ('3' , 'very high') ,
    ] , string ='Priority')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_consultation', 'In Consultation'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled'),
    ], default="draft" , string='State' , required=True , tracking=True)
    doctor_id = fields.Many2one('res.users' , string="Doctor" , tracking=True )
    pharmacy_line_ids = fields.One2many('appointment.pharmacy.lines', 'appointment_id' , string="pharmacy lines")
    hide_sales_price = fields.Boolean(string='hide sales price')
    operation_id = fields.Many2one('hospital.operation', string='operation')
    progress = fields.Integer(compute='_progress')

    @api.depends('state')
    def _progress(self):
        for rec in self:
            if rec.state == 'draft':
                progress = random.randrange(0 , 25)
            elif rec.state == 'in_consultation':
                progress = random.randrange(25 , 90)
            elif rec.state == 'done':
                progress = 100
            else :
                progress = 0
            rec.progress = progress


    @api.onchange('patient_id')
    def onchange_patient_id(self):
        self.ref =self.patient_id.ref


    def action_test(self):
        print("button clicked!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        return {
                'effect': {
                    'fadeout': 'slow',
                    'message': 'click success',
                    'type': 'rainbow_man',
                        }
                }
    @api.ondelete(at_uninstall=False)
    def check_doctor(self):
        for rec in self:
            if rec.doctor_id:
                raise UserError("you cand delete patient")

    def action_in_consultation(self):
        for rec in self:
            rec.state = "in_consultation"

    def action_done(self):
        for rec in self:
            rec.state = "done"

    def action_cancel(self):
        for rec in self:
            rec.state = "cancelled"

    def action_draft(self):
        for rec in self:
            rec.state="draft"

    class AppointmentPharmacyLines(models.Model):
        _name = "appointment.pharmacy.lines"
        _description = "Appointment pharmacy lines"

        product_id = fields.Many2one('product.product' , required=True)
        price_unit = fields.Float(string='Price' , related='product_id.list_price')
        qty = fields.Integer(string='Quantity' , default=1)
        appointment_id = fields.Many2one('hospital.appointment')


# class HideGroup(models.Model):
#     _inherit='res.groups'
#
#     def get_application_group(self , domain):
#         group_id = self.env.ref('').id
#         return super().HideGroup(domain + [('id' , '!=' , group_id)])

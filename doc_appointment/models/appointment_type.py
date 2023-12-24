from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class AppointmentType(models.Model):
    _inherit = "appointment.type"

    clinc_id = fields.Many2one("res.partner", string="Clinic Name")
    product_id = fields.Many2one("product.product", string="Product")
    price = fields.Float()
    photo = fields.Binary()
    about_service = fields.Text()
    tax_id = fields.Many2one('account.tax')
    service_id = fields.Many2one('service.category' , string='Service Category ')
    asset_id = fields.Many2many('asset.room')
    room_id = fields.Many2many('room.asset')
    payment_ids = fields.Many2one('account.payment')
    patient_rate_ids = fields.One2many('patient.rate', 'service_id', string='Customer')
    service_rt = fields.Float(compute='total_rate', store=True)

    # @api.depends('name')
    # def _compute_patient_rate(self):
    #     for rec in self:
    #         lines = []
    #         if rec.name:
    #             rates = self.env['patient.rate'].search([('service_id', '=', rec.name)])
    #             for service in rates:
    #                 vals = {
    #                     'user_id': service.user_id.id,
    #                     'rating': service.rating,
    #                     'desc': service.desc
    #                 }
    #                 lines.append((0, 0, vals))
    #         rec.update({'patient_rate_id': lines})


    @api.depends('patient_rate_ids')
    def total_rate(self):
        ln = {'1': 1, '2': 2, '3': 3, '4': 4, '5': 5}
        for rec in self:
            if rec.patient_rate_ids:
                total_patients = len(rec.patient_rate_ids)
                rate_100 = total_patients * 5
                rate = 0
                for patient in rec.patient_rate_ids:
                    rate += ln.get(patient.rating) if patient.rating else 0
                perc = (rate / rate_100) * 5
                rec.service_rt = perc
            else:rec.service_rt = 0

    def Total_price(self):
        for rec in self:
            if rec.patient.product_id:
                total_clinic = len(rec.patient.product_id)
                total = total_clinic * rec.patient.price
                print(total_clinic)
                print(total)



        # @api.onchange('product_id')
    # def _onchange_name(self):
    #     for rec in self:
    #         for service in rec.patient_rate_id:
    #             lines=[]
    #             vals = {
    #                 'user_id': service.user_id,
    #                 'rating': service.rating,
    #                 'desc': service.desc
    #             }
    #             print(">>>>>>>>>>>>>>>>>>.." , vals)
    #             lines.append((0 , 0 , vals))
    #             rec.patient_rate_id = lines

    # @api.depends('name')
    # def _com(self):
    #     print("...............", self.patient_rate_id)
    #     for rec in self:
    #         for service in rec.patient_rate_id:
    #             lines = []
    #             vals = {
    #                 'user_id': service.user_id,
    #                 'rating': service.rating,
    #                 'desc': service.desc
    #             }
    #             lines.append(vals)
    #             rec.patient_rate_id = lines



# appointment_datetime = fields.Datetime(string='Appointment Datetime', required=True)
#
# @api.constrains('clinc_id', 'appointment_datetime' , 'staff_user_ids')
# def _check_appointment_conflict(self):
#     for rec in self:
#         conflicting_appointments = self.search([
#             ('product_id', '=', rec.product_id.id),
#             ('appointment_datetime', '=', rec.appointment_datetime),
#             # ('staff_user_ids', '=', rec.staff_user_ids[0].id),
#             ('id', '!=', rec.id),
#             ])
#         if conflicting_appointments:
#             raise ValidationError("User is already booked for another service at the same time.")

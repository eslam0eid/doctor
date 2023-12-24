from odoo import fields , models , api

class HospitalOperation(models.Model):
    _name = 'hospital.operation'
    _log_access=False
    _rec_name = 'operation_name'

    doctor_id=fields.Many2one('res.users' , string='operation')
    operation_name = fields.Char(string='name')
    reference_record = fields.Reference(selection=[('hospital.patient' , 'Patient'),
                                                   ('hospital.appointment' , 'Appointment')], string='record')

    @api.model
    def name_create(self, name):
        return self.create({'name': name}).name_get()[0]
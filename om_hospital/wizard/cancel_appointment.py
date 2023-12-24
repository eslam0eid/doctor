from odoo import api , fields , models , _
from odoo.exceptions import UserError


class CancelAppointmentWizard(models.TransientModel):
    _name = "cancel.appointment.wizard"
    _description = "cancel Appointment wizard"
    # _log_access=False

    appointment_id = fields.Many2one('hospital.appointment' , string="Appointment")

    def action_cancel(self):
        # if self.appointment_id.booking_date == fields.day.today():
        #     raise UserError("sorry cancel not now")
        self.appointment_id.state= 'cancelled'
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }


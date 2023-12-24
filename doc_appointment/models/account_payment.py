from odoo import fields, models, api


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    meeting_id = fields.Many2one('calendar.event', readonly=True)


class AccountMove(models.Model):
    _inherit = 'account.move'

    meeting_id = fields.Many2one('calendar.event', readonly=True)

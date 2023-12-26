from odoo import models, fields, api
from datetime import timedelta


class Subscription(models.Model):
    _inherit = 'sale.order'

    warning_before = fields.Integer(string='Warning Before', default=7)

    def send_customer_mail(self):
        for sub in self.search([('is_subscription', '=', True), ('state', 'in', ['done', 'sale'])]):
            today = fields.Date.context_today(sub)
            # if today == sub.next_invoice_date - timedelta(days=sub.warning_before):
            sub.env['mail.mail'].sudo().create({
                                'body_html':sub.env['ir.config_parameter'].sudo().get_param('email_message'),
                                'subject': "you are booking an appointment with name  ",
                                'email_to': sub.partner_id.email,
                                'auto_delete': False,
                                }).send()


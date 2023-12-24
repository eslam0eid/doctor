from odoo import models, fields, api, _
import base64


class MeetingType(models.Model):
    _inherit = 'calendar.event'

    state = fields.Selection(selection=[('draft', 'Draft'), ('confirmed', 'confirmed')], default='draft', copy=False)
    pay_id = fields.Many2one('account.payment', readonly=True)
    jornal_id = fields.Many2one('account.move', readonly=True)
    patient_id = fields.Many2one('res.partner')

    # def btn_confirm(self):
    #     self.write({'state': 'confirmed'})

    @api.model
    def create(self, vals):
        res = super().create(vals)
        total_price = res.appointment_type_id.price + (
                res.appointment_type_id.price * res.appointment_type_id.tax_id.amount * 0.01)
        payment = self.env['account.payment'].sudo().create({'partner_id': res.patient_id.id,
                                                             'amount': total_price,
                                                             'meeting_id': res.id,
                                                             })

        res.pay_id = payment.id
        payment.action_post()
        if res.partner_ids:
            patient = res.partner_ids
            clinc = res.appointment_type_id.clinc_id
            if clinc.sale_order_ids and len(clinc.sale_order_ids) > 0:
                subscription = clinc.sale_order_ids[0]
                com_plan = subscription.commission_plan
            else:
                com_plan = 0
            amount = total_price
            amount_commission = (res.appointment_type_id.price * com_plan) / 100
            debit_line = {
                'account_id': patient.property_account_receivable_id.id,
                'partner_id': patient.id,
                'debit': amount,
                'credit': 0,
            }
            credit_line_1 = {
                'account_id': clinc.property_account_payable_id.id,
                'partner_id': clinc.id,
                'debit': 0,
                'credit': amount * 0.9,
            }
            credit_line_2 = {
                'account_id': self.env.ref("l10n_ae.3_uae_account_500001").id,
                'debit': 0,
                'credit': amount_commission,
                'tax_ids': self.env.ref('l10n_ae.3_uae_sale_tax_5_dubai'),
            }
            vals = {
                'move_type': 'entry',
                'meeting_id': res.id,
                'date': fields.Date.today(),
                'line_ids': [(0, 0, debit_line), (0, 0, credit_line_1), (0, 0, credit_line_2)]
            }
            entry = self.env['account.move'].sudo().create(vals)
            res.jornal_id = entry.id
            entry.action_post()
            return res

    def btn_confirm(self):
        self.write({'state': 'confirmed'})
        report = self.env.ref('doc_appointment.id_print_calender_event')
        report_service = report.sudo().report_name
        result, report_format = self.env['ir.actions.report'].sudo()._render_qweb_pdf(report, self.id)
        result = base64.b64encode(result)
        # if not report_service:
        #     report_service = 'report.' + report_service
        ext = "." + report_format
        # if not report_service.endswith(ext):
        report_service += ext
        value = {
            'datas': result,
            'name': report_service,
            'public': True,
        }
        attachment = self.env['ir.attachment'].sudo().create(value)
        url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        url += attachment.local_url

        self.env['mail.mail'].sudo().create({
            'email_from': self.env['res.users'].sudo().browse(2).email_formatted,
            'body_html': 'url : %s' % url,
            'subject': "you are booking an appointment with name  " ,
            'email_to': self.patient_id.email,
            'auto_delete': False,
        }).send()


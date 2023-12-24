from odoo.addons.portal.controllers.portal import CustomerPortal, pager
from odoo.http import request
from odoo import http
from odoo import _


class ClinicPortal(CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        values['patients_count'] = request.env['appointment.type'].search_count([])
        # if 'students' in counters:
        #     values['students'] = 5
        return values

    @http.route(['/my/appointment', '/my/appointment/page/<int:page>'], type='http', auth='user', website=True,
                sitemap=True)
    def PatientViewList(self, page=1, sortby='id', search="", search_in="All", clinc_id="",patient_id="", **kw):
        values = self._prepare_portal_layout_values()
        sorted_list = {
            'id': {'label': 'ID desc', 'order': 'id desc'},
            'name': {'label': 'name', 'order': 'name '},
        }
        search_list = {
            'All': {'label': 'ID desc', 'input': 'All', 'domain': []},
            'name': {'label': 'name', 'input': 'name ', 'domain': [('name', 'ilike', search)]},
        }
        default_sort_by = sorted_list[sortby]['order']
        search_domain = search_list[search_in]['domain']


        patient_obj = request.env['appointment.type']
        partner = request.env.user.partner_id
        clinic_records = request.env['calendar.event'].search([('patient_id', '=', patient_id)])
        # clinic_records = request.env['appointment.type'].sudo().search([('clinc_id', '=', patient_obj.meeting_ids.id)])
        # customer_records = request.env['appointment.type'].search([('clinc_id', '=', patient_obj.staff_user_ids.id)])
        total_order = 0
        appointment_count = len(clinic_records)
        print(clinic_records)
        print(appointment_count)
        for book in clinic_records:
            total_order += book.appointment_type_id.price
        total = appointment_count * total_order
        print(total)

        # customer_count = len(customer_records)
        # print(patient_obj.price)
        # print(patient_obj.staff_user_ids.id)
        # print(customer_count)
        # print(customer_records)

        # distinct_patient_ids = request.env['calendar.event'].sudo().search([('patient_id', '=', clinic_id)])
        # num_patients_registered = len(set(distinct_patient_ids))
        # print(num_patients_registered)

        # if 'patient_id' in clinc_id:
        #     if request.env['calendar.event'].sudo().search([('patient_id', '=', clinc_id)]):
        #         partner = request.env.user.partner_id
        #         values['patient_id'] = request.env['calendar.event'].search_count(partner)
        #     else:
        #         values['patient_id'] = 0
        # print(values)
        # return values

        total_patient = patient_obj.sudo().search_count(search_domain)
        page_details = pager(url='/my/appointment', total=total_patient, page=page,
                             url_args={'sortby': sortby, 'search_in': search_in, 'search': search},
                             step=5)
        patients = request.env['appointment.type'].search([], limit=5, order=default_sort_by,
                                                          offset=page_details['offset'])
        values.update({'patients': patients, 'page_name': 'patients_list',
                       # 'pager': page_details,
                       'sortby': sortby,
                       'clinic_id': total ,
                       'total':appointment_count,
                       'searchbar_sortings': sorted_list,
                       'search_in': search_in,
                       'search_bar_input': search_list,
                       'search': search
                       })
        return request.render('doc_appointment.patients_appointment_list_view', values)

    @http.route('/my/appointment/<model("appointment.type"):patient_id>', type='http', auth='user', website=True,
                sitemap=True)
    def PatientViewForm(self, patient_id, **kw):
        values = self._prepare_portal_layout_values()
        values.update({'patient': patient_id, 'page_name': 'patients_form'})
        patient_records = request.env['appointment.type'].search([])
        # customer_records = request.env['calendar.event'].search([('patient_id', '=', patient_id)])
        # total_price = 0
        # for book in customer_records:
        #     total_price += book.appointment_type_id.price
        # values['total'] = total_price
        patient_ids = patient_records.ids
        patient_index = patient_ids.index(patient_id.id)
        if patient_index != 0 and patient_ids[patient_index - 1]:
            values['prev_record'] = '/my/appointment/{}'.format(patient_ids[patient_index - 1])
        if patient_index < len(patient_ids) - 1 and patient_ids[patient_index + 1]:
            values['next_record'] = '/my/appointment/{}'.format(patient_ids[patient_index + 1])
        return request.render('doc_appointment.patients_appointment_form_view', values)



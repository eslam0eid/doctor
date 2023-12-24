from odoo.addons.portal.controllers.portal import CustomerPortal , pager
from odoo.http import request
from odoo import http
from odoo import  _


class LearnPortal(CustomerPortal):
    @http.route('/my/new/appointments' , auth='user' , type='http')
    def ViewPatient(self , **kw):

        return request.render('learn_portal.new_patient_form_portal', {})

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        values['patients_count'] = request.env['appointment.type'].search_count([])
        # if 'students' in counters:
        #     values['students'] = 5
        return values

    @http.route(['/my/appointments' , '/my/appointments/page/<int:page>' ], type='http', auth='user', website=True, sitemap=True)
    def PatientViewList(self,page = 1,sortby='id',search="" , search_in="All" ,groupby="none", **kw):
        values = self._prepare_portal_layout_values()

        sorted_list = {
            'id':{'label': 'ID desc' , 'order':'id desc'},
            'name':{'label': 'name' , 'order':'name '},
            'price':{'label': 'price' , 'order':'price '}
        }
        search_list = {
            'All': {'label': 'ID desc', 'input': 'All' , 'domain': []},
            'name': {'label': 'name', 'input': 'name ' , 'domain':[('name' , 'ilike' , search)]},
            'price': {'label': 'price', 'input': 'price ' , 'domain':[('price' , 'ilike' , search)]}
        }
        groupby_list = {
            'none': {'label': _('None'), 'input': 'none', 'order': 1},
            'name': {'label': _('Name'), 'input': 'name ', 'order': 1},
            'price': {'label': _('Price'), 'input': 'price', 'order': 1}
        }
        default_sort_by = sorted_list[sortby]['order']
        search_domain = search_list[search_in]['domain']
        patient_obj = request.env['appointment.type']
        total_patient = patient_obj.sudo().search_count(search_domain)
        page_details = pager(url='/my/appointments' , total=total_patient , page = page ,
                             url_args={'sortby':sortby , 'search_in':search_in , 'search':search , 'groupby':groupby} , step=3)
        patients = request.env['appointment.type'].search([] , limit=3 ,order=default_sort_by ,offset=page_details['offset'])
        values.update({'patients': patients , 'page_name' : 'patients_list' ,
                       'pager' : page_details ,
                       # 'default_url':'/my/appointments',
                       # 'groupby':groupby,
                       'sortby':sortby ,
                       'searchbar_sortings':sorted_list ,
                       # 'searchbar_groupby': groupby_list,
                       'search_in':search_in ,
                       'search_bar_input':search_list,
                       'search':search
                       })
        return request.render('learn_portal.patients_appointment_list_view', values)

    @http.route('/my/appointments/<model("appointment.type"):patient_id>', type='http', auth='user', website=True, sitemap=True)
    def PatientViewForm(self , patient_id , **kw):
        values = self._prepare_portal_layout_values()
        values.update({'patient' : patient_id , 'page_name' : 'patients_form'})
        patient_records = request.env['appointment.type'].search([])
        patient_ids = patient_records.ids
        patient_index = patient_ids.index(patient_id.id)
        if patient_index != 0 and patient_ids[patient_index - 1 ] :
            values['prev_record'] = '/my/appointments/{}'.format(patient_ids[patient_index - 1])
        if patient_index < len (patient_ids) - 1 and patient_ids[patient_index + 1]:
            values['next_record'] = '/my/appointments/{}'.format(patient_ids[patient_index + 1])

        return request.render('learn_portal.patients_appointment_form_view', values)

    @http.route('/my/appointments/print/<model("appointment.type"):patient_id>' , type='http' , auth='user' , website='true' , sitemap=True)
    def PatientReportPrint(self , patient_id , **kw):
        return self._show_report( model=patient_id, report_type='pdf', report_ref='doc_appointment.id_print_calender_event', download=True)

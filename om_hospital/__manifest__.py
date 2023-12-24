# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': 'hospital management',
    'version': '1.0.0',
    'category': 'hospital',
    'author': 'Eslam eid',
    'sequence': -100,
    'summary': 'hospital management system',
    'description': """hospital management system""",
    'depends': ['mail' , 'product' ,],
    'data': [
        'security/ir.model.access.csv',
        'data/sequence_data.xml',
        'wizard/cancel_appointment.xml',
        'views/patient_view.xml',
        'views/female_patient_view.xml',
        'views/male_patient_view.xml',
        'views/appointment_view.xml',
        'views/patient_tag.xml',
        'views/operation.xml',
        'views/menu.xml',

    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'assets': {},
    'license': 'LGPL-3',
}

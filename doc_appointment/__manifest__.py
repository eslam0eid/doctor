# -*- coding: utf-8 -*-
{
    'name': "Doctorak Appointment",
    'summary': """
    """,

    'description': """
        Long description of module's purpose
    """,
    'author': "Kaizen",
    'website': "http://www.yourcompany.com",
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['appointment', 'calendar', 'product', 'base', 'sale', 'account','sale_subscription', 'contacts'],

    # always loaded
    'data': [
        'security/patient_rate.xml',
        'security/ir.model.access.csv',
        'data/mail_template_data.xml',
        'data/sequence.xml',
        'views/portal.xml',
        'views/asset_room.xml',
        'views/room_asset.xml',
        'views/appointment_type.xml',
        'views/calendar_event.xml',
        'views/sale_order.xml',
        'views/res_partner.xml',
        'views/account_payment.xml',
        'views/journal.xml',
        'views/patient_rating.xml',
        'views/service_category.xml',

    ],
}

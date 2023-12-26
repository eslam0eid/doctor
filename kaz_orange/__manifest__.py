# -*- coding: utf-8 -*-
{
    'name': "kaz orange",
    'summary': """
    """,

    'description': """
        send email to the user
    """,
    'author': "kaizen",
    'website': "http://www.yourcompany.com",
    'category': 'orange',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['sale' , 'sale_subscription' , 'mail'],

    # always loaded
    'data': [
        'views/sale_order.xml',
        'views/res_config_settings_views.xml',
    ],
}

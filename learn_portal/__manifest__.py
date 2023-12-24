# -*- coding: utf-8 -*-
{
    'name': "learn portal",
    'summary': """
    """,

    'description': """
        Long description of module's purpose
    """,
    'author': "eslam",
    'website': "http://www.yourcompany.com",
    'category': 'portal',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['doc_appointment','portal'],

    # always loaded
    'data': [
        'views/portal_templete.xml',
    ],
}

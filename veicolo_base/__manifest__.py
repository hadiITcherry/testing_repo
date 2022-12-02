# -*- coding: utf-8 -*-
{
    'name': "Veicolo",

    'summary': """It is the base module for Veicolo Platform
    """,

    'description': """
       The Base Module for Veicolo Platform
    """,

    'author': "IT Cherry",
    'website': "http://www.itcherry.net",

    'category': '/Veicolo',
    'version': '0.1',

    'depends': ['base', 'veicolo_product'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/vehicle_brand_model_views.xml',
        'views/product_template_view.xml',
        'data/veicolo_base_vehicle_data.xml',
        'data/veicolo_base_data.xml',
        'data/mail_data.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],

    'assets': {
        'web.assets_backend': [
            'veicolo_base/static/src/**/*',
        ],
    },
    'license': 'LGPL-3',
    'auto_install': True,
    'installable': True,
}

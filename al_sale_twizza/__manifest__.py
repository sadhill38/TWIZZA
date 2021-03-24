# -*- coding: utf-8 -*-
###################################################################################
#
#    @lahlou apps
#
#    Copyright (C) 2021 alahlou.com
#
###################################################################################
{
    'name': "@lahlou : Sale Twizza",

    'summary': """
        Customisations in sale module for twizza.""",

    'description': """
        Customisations in sale module for twizza.
    """,

    'author': "Ahmed LAHLOU, @lahlou",
    'website': "https://alahlou.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full listhr
    'category': 'sale',
    'version': '13.0.0.1',

    'depends': [
        'sale',
        'sale_stock',
        'sale_margin',
    ],

    # always loaded
    'data': [
        'security/security.xml',
        # 'security/ir.model.access.csv',
        'views/sale_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
    'qweb': [
        # 'static/src/xml/file.xml',
    ],
    'application': True,
    'sequence': 2,
}

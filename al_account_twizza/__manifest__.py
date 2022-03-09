# -*- coding: utf-8 -*-
###################################################################################
#
#    @lahlou apps
#
#    Copyright (C) 2021 alahlou.com
#
###################################################################################
{
    'name': "@lahlou : Account Twizza",

    'summary': """
        Customisations in account module for twizza.
    """,

    'description': """
        Customisations in account module for twizza.
    """,

    'author': "Ahmed LAHLOU, @lahlou",
    'website': "https://alahlou.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full listhr
    'category': 'account',
    'version': '13.0.0.1',

    'depends': [
        # odoo addons
        'account',
        'account_followup',
        'account_reports',
        'purchase',
        'stock',
        # twizza addons
        'al_sale_twizza',
    ],

    # always loaded
    'data': [
        # security
        'security/security.xml',
        'security/ir.model.access.csv',
        # views
        'views/account_views.xml',
        'views/partner_views.xml',
        # menus
        'views/menuitems.xml',
    ],

    # only loaded in demonstration mode
    'demo': [

    ],

    'qweb': [
        # 'static/src/xml/file.xml',
    ],

    'application': True,

    'sequence': 2,
}
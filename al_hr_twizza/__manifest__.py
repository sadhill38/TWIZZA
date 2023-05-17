# -*- coding: utf-8 -*-
###################################################################################
#
#    @lahlou apps
#
#    Copyright (C) 2021 alahlou.com
#
###################################################################################
{
    'name': "@lahlou : HR Twizza",

    'summary': """
        HR custom features.
    """,

    'description': """
        HR custom features.
    """,

    'author': "Ahmed LAHLOU, @lahlou",
    'website': "https://alahlou.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full listhr
    'category': 'Human Resources/Employees',
    'version': '13.0.0.1',

    'depends': [
        # odoo
        'hr',
        'hr_holidays',
        # oca
        'hr_holidays_public',
    ],

    # always loaded
    'data': [
        # Views
    ],

    'application': True,
    'sequence': 2,
}

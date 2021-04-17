# -*- coding: utf-8 -*-
###################################################################################
#
#    @lahlou apps
#
#    Copyright (C) 2021 alahlou.com
#
###################################################################################
{
    'name': "@lahlou : Twizza Dashboard",

    'summary': """
        Add Customized Dashboards for Twizza.""",

    'description': """
        Add Customized Dashboards for Twizza.
    """,

    'author': "Ahmed LAHLOU, @lahlou",
    'website': "https://alahlou.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full listhr
    'category': 'report',
    'version': '13.0.0.2',

    'depends': [
        'base',
        'board',
        'al_sale_twizza',
        'web_pivot_computed_measure',
    ],

    # always loaded
    'data': [
        # Security
        'security/security.xml',
        'security/ir.model.access.csv',
        # Views
        'views/sales_report.xml',
        # menus : keep last
        'views/menuitems.xml',
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

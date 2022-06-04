# import xmlrpc.client
#
# # prod credentials
# url = 'http://localhost:3013'
# user = 'admin'
# password = 'admin'
# db = 'prod_2022_05_18'
#
# # script
# common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url), allow_none=True)
# uid = common.authenticate(db, user, password, {})
#
# models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url), allow_none=True)
#
# # ####### STEP 1
# # copy_products_translation = models.execute_kw(
# #     db, uid, password, 'ir.translation', 'search_read', [[
# #         ['src', 'ilike', 'copie'],
# #         ['name', '=', 'product.template,name'],
# #         ['lang', '=', 'fr_FR'],
# #     ]], {'fields': ['res_id', 'src', 'value']}
# # )
# #
# # for trans in copy_products_translation:
# #     print(trans)
# #     models.execute_kw(
# #         db, uid, password, 'product.template', 'write', [[trans['res_id']], {'name': trans['value']}]
# #     )
#
# # ####### STEP 2
# fix_product_template_translation = models.execute_kw(
#     db, uid, password, 'ir.translation', 'search_read', [[
#         ['name', '=', 'product.template,name'],
#         ['lang', '=', 'en_US'],
#     ]], {'fields': ['res_id', 'src', 'value']}
# )
#
# for en_trans in fix_product_template_translation:
#     print(en_trans)
#     # todo : uncomment this to execute
#     models.execute_kw(
#         db, uid, password, 'ir.translation', 'write', [[en_trans['id']], {
#             'value': en_trans['src'],
#         }]
#     )
#
# print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
# # print(len(copy_products_translation))
# print(len(fix_product_template_translation))
# print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

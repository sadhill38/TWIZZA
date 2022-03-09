from odoo import fields, models, api


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    ftp_host = fields.Char(string="FTP HOST", config_parameter='ftp_host')
    ftp_user = fields.Char(string="FTP USER", config_parameter='ftp_user')
    ftp_password = fields.Char(string="FTP PASSWORD", config_parameter='ftp_password')
    ftp_port = fields.Char(string="FTP PORT", config_parameter='ftp_port')
    local_path = fields.Char(string="LOCAL PATH", config_parameter='local_path')

    @api.model
    def _ftp_sync_database(self):
        # todo : make this function
        return True

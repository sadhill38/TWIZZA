from odoo import fields, models, api, exceptions, _
from datetime import timedelta


class HrLeave(models.Model):
    _inherit = "hr.leave"

    @api.constrains('date_from', 'holiday_status_id', 'employee_id')
    def _check_period_before_leave_request(self):
        for leave in self:
            if (
                leave.holiday_status_id.validation_type in ["hr", "both"]
                and leave.holiday_status_id.responsible_id != leave.employee_id.user_id
            ):
                allowed_date_from = fields.Datetime.today() + timedelta(days=30)
                if leave.date_from < allowed_date_from:
                    raise exceptions.ValidationError(_(
                        "you must request your leave from : %s\n"
                        "If you want a date before that, you should ask your HR manager."
                    ) % allowed_date_from.strftime("%d/%m/%Y"))

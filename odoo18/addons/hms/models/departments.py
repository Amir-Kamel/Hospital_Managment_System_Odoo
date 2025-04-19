from odoo import models, fields


class HmsDepartment(models.Model):
    _name = 'hms.department'

    name = fields.Char(required=True)
    capacity = fields.Integer()
    is_open = fields.Boolean(default=True)
    patient_ids = fields.One2many('hms.patient', 'department_id')

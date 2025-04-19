from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date
import re

class HmsPatient(models.Model):
    _name = 'hms.patient'
    _rec_name = 'first_name'

    first_name = fields.Char(required=True)
    last_name = fields.Char(required=True)
    department_id = fields.Many2one('hms.department')
    department_capacity = fields.Integer(related='department_id.capacity', readonly=True)
    doctor_ids = fields.Many2many('hms.doctor')
    readonly_doctors = fields.Boolean(compute='_compute_readonly_doctors', store=False)
    birth_date = fields.Date()
    history = fields.Html()
    cr_ratio = fields.Float()
    blood_type = fields.Selection([
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ])
    pcr = fields.Boolean()
    image = fields.Image()
    address = fields.Text()
    age = fields.Integer(compute='_compute_age', store=True)
    states = fields.Selection([
        ('undetermined', 'Undetermined'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('serious', 'Serious'),
    ])
    log_ids = fields.One2many('hms.patient.log', 'patient_id')
    email = fields.Char(string='Email', required=True, unique=True)

    @api.depends('birth_date')
    def _compute_age(self):
        for rec in self:
            if rec.birth_date:
                today = date.today()
                rec.age = today.year - rec.birth_date.year - (
                        (today.month, today.day) < (rec.birth_date.month, rec.birth_date.day)
                )
            else:
                rec.age = 0


    @api.depends('department_id')
    def _compute_readonly_doctors(self):
        for patient in self:
            patient.readonly_doctors = not bool(patient.department_id)

    @api.onchange('department_id')
    def _onchange_department_log(self):
        if self.department_id:
            self.env['hms.patient.log'].create({
                'patient_id': self.id,
                'description': f"Department changed to {self.department_id.name}",
            })

    @api.constrains('email')
    def _check_email(self):
        for rec in self:
            if rec.email:
                if not re.match(r"[^@]+@[^@]+\.[^@]+", rec.email):
                    raise ValidationError("Please enter a valid email address.")

                existing = self.search([('email', '=', rec.email), ('id', '!=', rec.id)])
                if existing:
                    raise ValidationError("Email must be unique.")

    @api.onchange('age')
    def _onchange_age_check_pcr(self):
        if self.age and self.age < 30:
            if not self.pcr:
                self.pcr = True
                return {
                    'warning': {
                        'title': "PCR Checked",
                        'message': "PCR has been automatically checked because the age is below 30."
                    }
                }
        elif self.age and self.age >= 30:
            if self.pcr:
                self.pcr = False
                return {
                    'warning': {
                        'title': "PCR Unchecked",
                        'message': "PCR has been automatically unchecked because the age is 30 or above."
                    }
                }
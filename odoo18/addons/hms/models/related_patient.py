from odoo import models, fields,  exceptions, api ,_
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    related_patient_id = fields.Many2one('hms.patient')

    def unlink(self):
        for partner in self:
            if partner.related_patient_id:
                raise exceptions.UserError(
                    _("You cannot delete a customer who is linked to a patient.")
                )
        return super(ResPartner, self).unlink()

    @api.constrains('related_patient_id')
    def _check_patient_email_conflict(self):
        for record in self:
            if record.related_patient_id and record.email:
                patient_email = record.related_patient_id.email
                if patient_email and patient_email == record.email:
                    raise ValidationError(
                        "You cannot link a customer to a patient with the same email address."
                    )

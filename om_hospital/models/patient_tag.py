from odoo import api , fields , models


class PatientTag(models.Model):
    _name = "patient.tag"
    _description = "patient tag"

    name = fields.Char(string='Name', required=True ,tracking=True)
    active = fields.Boolean(string="Active", default='true', tracking=True)
    color = fields.Integer(string="color")
    color_2 = fields.Char(string="color 2")

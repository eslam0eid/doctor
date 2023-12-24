from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    clinic = fields.Boolean(string='Is Clinic', default=True)
    cover = fields.Binary(string='cover photo')
    experience_years = fields.Integer(string='Experience years')
    expertise = fields.Text(string='Expertise')

    about_clinic = fields.Text(string = 'About Clinic ')


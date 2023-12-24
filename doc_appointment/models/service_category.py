from odoo import fields , models

class Service_category(models.Model):
    _name = 'service.category'

    name = fields.Char(string='Name' , required=True)
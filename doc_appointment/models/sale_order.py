from odoo import models , fields ,api

class percentage(models.Model):
    _inherit ='sale.order'

    commission_plan = fields.Float(string='Commission plan')



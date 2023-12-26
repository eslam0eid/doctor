# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    warning_before = fields.Integer(string='Warning Before', default=7, config_parameter='kaz_orange.warning_before')
    email_message = fields.Text()

    @api.model
    def set_values(self):
        config_param = self.env['ir.config_parameter']
        config_param.sudo().set_param('email_message', self.email_message)
        res = super(ResConfigSettings, self).set_values()
        return res

    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        config_param = self.env['ir.config_parameter']
        email_message = config_param.sudo().get_param('email_message')
        res.update(
            email_message=str(email_message),

        )
        return res

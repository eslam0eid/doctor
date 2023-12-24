from odoo import fields , models , _

class AssetRoom(models.Model):
    _name = 'room.asset'


    name = fields.Many2one('calendar.event' , string='Name', required=True)
    # name = fields.Many2one(related='name_id.partner_ids.name')

    clinc_id = fields.Many2one("res.partner", string="Clinic Name")
    room_id = fields.Char(default="Room" , string='is Room')

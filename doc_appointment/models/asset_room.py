from odoo import fields , models , api , _

class AssetRoom(models.Model):
    _name = 'asset.room'

    name = fields.Many2one('calendar.event' , string='Name', required=True)
    # name = fields.Many2one(related='name_id.partner_ids.name')

    clinc_id = fields.Many2one("res.partner", string="Clinic Name")
    asset_id = fields.Char(default="Asset" , string='is Asset')

    asset = fields.Selection([
        ('asset', 'Asset'),
        ('room', 'Room')] , string='type')
    assets_Rooms_id = fields.One2many('asset.room.lines','asset_id')




class AssetRoomLines(models.Model):
    _name = 'asset.room.lines'


    asset = fields.Selection([
        ('asset', 'Asset'),
        ('room', 'Room')] , string='type')
    asset_id = fields.Many2one('asset.room')
    asset_name = fields.Char(string='name')

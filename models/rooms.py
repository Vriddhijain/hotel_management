from odoo import models, fields

class Rooms(models.Model):
    _name = 'rooms.room'
    _description = 'Hotel Rooms'

    name = fields.Char(string="Room Number")
    type_id = fields.Many2one('rooms.types', string="Type")
    floor_id = fields.Many2one('room.floor', string="Floor")
    hotel = fields.Char(string='Hotel', related='floor_id.hotel', store=True, readonly=True)
    charge = fields.Float(string="Charge", related='type_id.charge', store=True, readonly=True)
    status = fields.Selection([
        ('vacant', 'Vacant'),
        ('occupied', 'Occupied')
    ], string="Status", default='vacant')
    hotel_id = fields.Many2one('add.hotel', string='Hotel', ondelete='cascade')

   

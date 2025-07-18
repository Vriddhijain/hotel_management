from odoo import models, fields


class RoomsFloor(models.Model):
 
   _name = 'room.floor'
   _description = 'Rooms Floor'
   
   name=fields.Char(string='Name')
   hotel=fields.Char(string='Hotel')
   hotel_id = fields.Many2one('add.hotel', string='Hotel', ondelete='cascade')
   
   



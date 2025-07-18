from odoo import models, fields, api

class RoomWizard(models.TransientModel):
    _name = 'room.wizard'
    _description = 'Room Generation Wizard'


    room_ids = fields.Many2many( 'rooms.room', string='Rooms', readonly=True, default=lambda self: self.env['rooms.room'].search([]).ids)

    
    
    def generate_rooms(self):
        active_id = self.env.context.get('active_id')
        if active_id:
            hotel = self.env['add.hotel'].browse(active_id)
            self.room_ids.write({'hotel_id': hotel.id})
            hotel.is_room_generated = True  
        return {'type': 'ir.actions.act_window_close'}
  
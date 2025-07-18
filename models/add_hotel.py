from odoo import models, fields,api
from odoo.exceptions import ValidationError
import re


class HotelManagementSystem(models.Model):
 
   _name = 'add.hotel'
   _description = 'Hotel'
   _rec_name='hotel_name'
    
   hotel_name=fields.Char(string="Name")
   address=fields.Text(string='Address')
   gstin=fields.Char(string='GSTIN')
   total_floor=fields.Integer(string='Total Floor')
   total_rooms=fields.Integer(string='Total Room')
   phone=fields.Char(string='Phone')
   mobile=fields.Char(string='Mobile')
   email=fields.Char(string="Email")
   website=fields.Char(string='Website')
   priority=fields.Char(string='Priority')
   manager=fields.Char(string='Manager')
   check_in_out=fields.Datetime(string="Check in / OUT Time")
   
 
   floor_ids = fields.One2many('room.floor', 'hotel_id', string='Floors')
   room_ids = fields.One2many('rooms.room', 'hotel_id', string='Rooms')
#    name = fields.One2many('rooms.room', 'room_name', string='Name')
   is_floor_generated = fields.Boolean(string='Is Floor Generated', default=False)
   is_room_generated = fields.Boolean(string='Is Room Generated', default=False)
   amenities_ids = fields.One2many('amenities', 'hotel_id', string="Amenities")
   photo=fields.Binary(string="Photo")

   _sql_constraints = [
        ('unique_gstin', 'unique(gstin)', 'GSTIN must be unique!'),
        ('unique_name', 'unique(hotel_name)', 'Hotel name must be unique!'),
    ]
   @api.constrains('email')
   def _check_email(self):
        for record in self:
            if record.email and not re.match(r"[^@]+@[^@]+\.[^@]+", record.email):
                raise ValidationError("Enter a valid email address.")

   def action_generate_floors(self):
        for hotel in self:
            records = self.env['room.floor'].search([('hotel_id', '=', False)])
            records.write({'hotel_id': hotel.id})
        self.is_floor_generated = True
        
   @api.constrains('phone', 'mobile')
   def _check_phone_mobile(self):
        for record in self:
            for field in ['phone', 'mobile']:
                value = getattr(record, field)
                if value and not re.match(r'^\+?\d{7,15}$', value):
                    raise ValidationError(" must be a valid phone number (7-15 digits).")
                
   @api.constrains('total_floor', 'total_rooms')
   def _check_positive_numbers(self):
        for record in self:
            if record.total_floor <= 0:
                raise ValidationError("Total floors must be a positive integer.")
            if record.total_rooms <= 0:
                raise ValidationError("Total rooms must be a positive integer.")
            
            
   def action_open_room_wizard(self):
        self.is_room_generated= True
        return {
            'type': 'ir.actions.act_window',
            'name': 'All Rooms',
            'res_model': 'room.wizard',
            'view_mode': 'form',
            'target': 'new',
            
        }
            
   def action_view_floors(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Floors',
            'res_model': 'room.floor',  
            'domain': [('hotel_id', '=', self.id)],
            'view_mode': 'list,form',
            'target': 'current',
            
        }

   def action_view_rooms(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Floors',
            'res_model': 'rooms.room',  
            'domain': [('hotel_id', '=', self.id)],
            'view_mode': 'list,form',
            'target': 'current',
            
        }
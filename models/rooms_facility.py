from odoo import models, fields


class RoomsFacility(models.Model):
 
   _name = 'rooms.facility'
   _description = 'Rooms Facility'
   
   name=fields.Char(string='Facility Name')
   rooms_facility_image=fields.Image(string="Add")


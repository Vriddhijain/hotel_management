from odoo import models, fields


class HotelManagementSystem(models.Model):
 
   _name = 'hotel.management'
   _description = 'Hotel Management System'
   
   name=fields.Char(string='Name')

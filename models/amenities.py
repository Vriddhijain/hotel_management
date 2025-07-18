from odoo import models, fields


class Ameneities(models.Model):
 
   _name = 'amenities'
   _description = 'Amenities'

   amenities_name=fields.Char(string='Hotel Amenities')
   charge_type=fields.Integer(string="Charge Type")
   hotel_id = fields.Many2one('add.hotel', string="Hotel")
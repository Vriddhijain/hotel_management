from odoo import models, fields


class Customer(models.Model):
 
   _name = 'staff'
   _description = 'Staff'
   
   
   
   staff_name=fields.Char(string="Name")
   staff_email=fields.Char(string="Email")
   staff_address=fields.Text(string="Address")
   staff_mobile=fields.Char(string="Mobile")
   staff_phone=fields.Char(string="Phone")
   staff_photo=fields.Binary(string="Photo")
   
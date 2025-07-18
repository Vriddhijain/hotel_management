from odoo import models, fields

class TransportServices(models.Model):
    _name = 'transport.services'
    _description = 'Transport Services'
    
    
    
    name=fields.Char(String="Name")
    mobile=fields.Char(string="Mobile")
    hotel_id=fields.Many2one('add.hotel', string='Hotel')
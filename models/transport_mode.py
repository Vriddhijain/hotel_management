from odoo import models, fields

class TransportServices(models.Model):
    _name = 'transport.mode'
    _description = 'Transport Mode'
    
    
    
    name=fields.Char(String="Name")
    hotel_id=fields.Many2one('add.hotel', string='Hotel')
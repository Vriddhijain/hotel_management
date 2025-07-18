from odoo import models,fields,api

class PickupDestinationModel(models.Model):
    _name = 'pickup.destination'
    _description = 'Pickup Destination Model'
    
    
    name=fields.Char(string="Name")
    hotel_id=fields.Many2one('add.hotel', string='Hotel')
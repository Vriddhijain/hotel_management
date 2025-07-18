from odoo import models,fields,api

class InquiryModel(models.Model):
    _name = 'inquiry.mode'
    _description = 'Inquiry Mode'
    
    
    name=fields.Char(string="Name")
    hotel_id=fields.Many2one('add.hotel', string='Hotel')
    
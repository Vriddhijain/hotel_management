from odoo import models, fields


class HotelSeasonablePrice(models.Model):
    _name = 'hotel.seasonable.price'
    _description = 'Seasonable Price'

    room_id = fields.Many2one('rooms.types', string="Room")
    seasonable_name = fields.Char(string='Name')
    start_date = fields.Datetime(string="Start Date")
    end_date = fields.Datetime(string="End Date")
    special_charge = fields.Integer(string="Special Charge")
    active = fields.Boolean(string="Active")

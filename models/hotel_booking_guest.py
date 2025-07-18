from odoo import models, fields
class HotelBookingGuest(models.Model):
    _name = 'hotel.booking.guest'
    _description = 'Hotel Booking Guest'

    name = fields.Char(string='Guest Name')
    age = fields.Integer(string='Age')
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string='Gender')
    contact=fields.Char(string="Contact")
    booking_id = fields.Many2one('hotel.booking', string='Booking')
    fields.Many2one('rooms.types', string="Room")
    type=fields.Char(string="Type")
    lead_id = fields.Many2one('crm.lead', string="Lead")

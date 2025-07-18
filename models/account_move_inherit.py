from odoo import models, fields

class AccountMove(models.Model):
    _inherit = 'account.move'

    hotel_booking_id = fields.Many2one('hotel.booking', string="Hotel Booking")

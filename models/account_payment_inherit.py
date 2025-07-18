from odoo import models, fields

class AccountPayment(models.Model):
    _inherit = 'account.payment'

    hotel_booking_id = fields.Many2one('hotel.booking', string="Hotel Booking")

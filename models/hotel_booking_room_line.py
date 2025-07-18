from odoo import models, fields,api


class HotelBookingRoomLine(models.Model):
    _name = 'hotel.booking.room.line'
    _description = 'Hotel Booking Room Line'

    booking_id = fields.Many2one('hotel.booking', string='Booking Reference', ondelete='cascade')
    room_type_id = fields.Many2one('rooms.types', string='Room Type')
    room_type_id_lead = fields.Many2one('rooms.types', string='Room Type')
    lead_id_booking = fields.Many2one('crm.lead', string='Lead Booking Reference', ondelete='cascade')
    quantity = fields.Integer(string='Quantity')
    day = fields.Integer(string='Day')
    charges = fields.Float(string='Charges')
    tax_percent = fields.Float(string='Tax (%)', default=15.0)
    amount_total = fields.Float(string='Total Amount', compute='_compute_amount_total', store=True)
    # total_amount = fields.Float(string='Total Amount', compute='_compute_total', store=True)
    currency_id = fields.Many2one(related='booking_id.currency_id', store=True, readonly=False)
    room_charge = fields.Float(string="Room Charge", compute='_compute_amount_total', store=True)
    subtotal = fields.Float(string="Sub Total", compute='_compute_amount_total', store=True)
    tax_amount = fields.Float(string="Tax Amount", compute='_compute_amount_total', store=True)
    lead_rooms_id = fields.Many2one('crm.lead', string='Rooms')


    @api.onchange('room_type_id')
    def _onchange_room_type(self):
        if self.room_type_id:
            self.charges = self.room_type_id.charge

    @api.onchange('booking_id')
    def _onchange_booking_id(self):
        if self.booking_id:
            self.day = self.booking_id.total_days or 0
            self.quantity = self.booking_id.total_rooms or 0
            
    @api.depends('quantity', 'charges', 'day', 'tax_percent')
    def _compute_amount_total(self):
        for rec in self:
            rec.room_charge = rec.charges
            rec.subtotal = rec.charges * rec.day * rec.quantity
            rec.tax_amount = rec.subtotal * (rec.tax_percent / 100.0)
            rec.amount_total = rec.subtotal + rec.tax_amount


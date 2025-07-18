from odoo import models, fields,api

class LeadInquiry(models.Model):
    _inherit = 'crm.lead'
    _description = 'Lead Inquiry'

    hotel = fields.Many2one('add.hotel',string='Hotel')    
    checkin_date = fields.Datetime(string='Check In Date')
    checkout_date = fields.Datetime(string='Check Out Date')
    inquiry_mode = fields.Many2one('inquiry.mode', string='Inquiry Mode')
    

    guest_name=fields.Char(string='Name')
    guest_age=fields.Char(string='Age')
    guest_type=fields.Char(string='Type')
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string='Gender')
    contact=fields.Char(string="Contact")
    guest_ids = fields.One2many('hotel.booking.guest', 'lead_id', string="Guest Details")
    lead_id_room_booking=fields.One2many('hotel.booking.room.line', 'lead_id_booking', string='Rooms')
    

    
    def action_create_booking(self):
        # import pdb;pdb.set_trace()
        self.ensure_one()
        guest_lines = []
        for guest in self.guest_ids:
            guest_lines.append((0, 0, {
                'name': guest.name,
                'age': guest.age,
                'gender': guest.gender,
                'contact': guest.contact,
            }))
        room_lines = []
        for room in self.lead_id_room_booking:
            room_lines.append((0, 0, {
                'room_type_id': room.room_type_id_lead.id, 
                'quantity': room.quantity,
                'day': room.day,
                'charges': room.charges,
                'tax_percent': room.tax_percent,
                'amount_total': room.amount_total,
            }))
        return {
            'type': 'ir.actions.act_window',
            'name': 'Create Booking',
            'res_model': 'hotel.booking',
            'view_mode': 'form',
            'target': 'new',
            'context': {            
                'default_partner_id': self.partner_id.id,
                'default_hotel_id': self.hotel.id,            
                'default_checkin_date': self.checkin_date,
                'default_checkout_date': self.checkout_date,
                'default_guest_ids': guest_lines, 
                'default_room_line_ids': room_lines,
            }
        }
        
    
    
    
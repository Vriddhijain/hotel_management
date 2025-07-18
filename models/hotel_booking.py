from odoo import models, fields,api
from odoo.exceptions import UserError, ValidationError
import re

class HotelBooking(models.Model):
    _name = 'hotel.booking'
    _inherit=['mail.thread', 'mail.activity.mixin']
    _description = 'Hotel Booking'

    name = fields.Char(string='Booking Reference', default='New',readonly=True, copy=False)
    # customer_id = fields.Many2one('customer', string='Customer', required=True)
    address=fields.Text(string='Address')
    email=fields.Char(string='Email')
    phone=fields.Char(string='Phone')
    mobile=fields.Char(string='Mobile')
    checkin_date = fields.Datetime(string='Check In Date')
    checkout_date = fields.Datetime(string='Check Out Date')
    booking_date = fields.Date(string='Booking Date', default=fields.Date.today)
    total_days = fields.Integer(string='Total Day',default=0)
    inquiry_mode = fields.Selection([('email', 'Email'), ('phone', 'Phone')], string='Inquiry Mode')
    payment_state = fields.Selection([('draft', 'Draft'), ('confirmed', 'Confirmed'), ('invoiced', 'Invoice Generated'),('paid','Paid'), ('cancelled', 'Cancelled')], default='draft')
    
    hotel_id = fields.Many2one('add.hotel', string='Hotel')
    guest_pickup = fields.Boolean(string='Guest Pickup')
    total_rooms=fields.Integer(string="Total Rooms" ,default=0)
    adult=fields.Integer(string="Adult")
    child=fields.Integer(string="Child")
    rooms=fields.Integer(string="Rooms")
    room_type = fields.Selection([('standard', 'Standard double room')], string='Room Type')
    quantity = fields.Integer(string='Quantity')
    day=fields.Integer(string='Day')
    charges = fields.Float(string='Charges')
    tax_percent = fields.Float(string='Tax (%)', default=15.0)
    room_line_ids = fields.One2many('hotel.booking.room.line', 'booking_id', string='Rooms')
    guest_ids = fields.One2many('hotel.booking.guest', 'booking_id', string='Guests')
    pickup_service_type=fields.Many2one('transport.services',string="Pickup Service Type")
    driver=fields.Char(string="Driver")
    transport_mode=fields.Many2one('transport.mode',string="Transport Mode")
    pickup_location=fields.Many2one('pickup.destination',string="Pickup Location")
    pickup_destination=fields.Many2one('pickup.destination',string="Pickup Destination")
    # document_name = fields.Char(string="Document Name")
    # document_file = fields.Binary(string="Upload Document")
    policy_id = fields.Many2one('policy.template', string="Policy")
    policy_details = fields.Text(related='policy_id.policy_details', string="Policy Details")
    amount_total = fields.Monetary(string="Untaxted Amount", compute='_compute_amount_total', store=True)
    # amount_tax = fields.Monetary(string='Tax', compute='_compute_amount_total', store=True)
    # amount_total = fields.Monetary(string='Untaxted Amount', compute='_compute_amount_total', store=True)
    currency_id = fields.Many2one('res.currency', string='Currency', required=True, default=lambda self: self.env.company.currency_id)
    partner_id = fields.Many2one('res.partner', string="Customer", required=True)
    # invoice_id = fields.Many2one('hotel.invoice', string="Invoice")
    payment_id = fields.Many2one('hotel.payment', string="Payment")
    invoice_id = fields.Many2one('account.move', string="Invoice" ,  ondelete='set null')
    room_charge = fields.Float(string="Room Charge", compute='_compute_amount_total', store=True)
    subtotal = fields.Float(string="Sub Total", compute='_compute_amount_total', store=True)
    tax_amount = fields.Float(string="Tax Amount", compute='_compute_amount_total', store=True)
    attachment_ids = fields.Many2many(
        'ir.attachment',
        'hotel_booking_ir_attachments_rel',
        'booking_id', 'attachment_id',
        string='Documents',
        domain=[('res_model', '=', 'hotel.booking')],
    )
    lead_id = fields.Many2one('crm.lead', string='Lead Reference')



    
    @api.constrains('email')
    def _validate_email(self):
        for rec in self:
            if rec.email and not re.match(r"[^@]+@[^@]+\.[^@]+", rec.email):
                raise ValidationError("Enter a valid email address.")
            
    @api.constrains('checkin_date', 'checkout_date')
    def _validate_dates(self):
        for rec in self:
            if rec.checkin_date and rec.checkout_date:
                if rec.checkin_date >= rec.checkout_date:
                    raise ValidationError("Check-out date must be after check-in date.")
                
    @api.constrains('phone', 'mobile')
    def _check_phone_numbers(self):
        for rec in self:
            for field in ['phone', 'mobile']:
                value = getattr(rec, field)
                if value and not re.match(r'^\+?\d{7,15}$', value):
                    raise ValidationError(" must be a valid phone number (7–15 digits).")



    @api.depends('room_line_ids.amount_total')
    def _compute_amount_total(self):
        for rec in self:
            rec.room_charge = sum(line.charges for line in rec.room_line_ids)
            rec.subtotal = sum(line.charges * line.quantity * line.day for line in rec.room_line_ids)
            rec.tax_amount = sum((line.charges * line.quantity * line.day) * (line.tax_percent / 100.0) for line in rec.room_line_ids)
            rec.amount_total = rec.subtotal + rec.tax_amount

    
    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        if self.partner_id:
            self.address = self.partner_id.contact_address
            self.email = self.partner_id.email 
            self.phone = self.partner_id.phone 
            self.mobile = self.partner_id.mobile 
    
    def action_confirm(self):
        self.payment_state = 'confirmed'

        
    def action_cancel(self):
        self.payment_state = 'cancelled'
        
        
    # @api.onchange('guest_pickup')
    # def _onchange_guest_pickup(self):
    #     if self.guest_pickup:
    #         unassigned_guests = self.env['hotel.booking.guest'].search([('booking_id', '=', False)])
    #         for guest in unassigned_guests:
    #             guest.write({'booking_id': self.id})
                


    def create_payment(self):
        for booking in self:
            if not booking.invoice_id:
                raise UserError("No invoice found. Please create an invoice first.")

            if booking.invoice_id.state != 'posted':
                booking.invoice_id.action_post()

            payment_register = self.env['account.payment.register'].with_context(
                active_model='account.move',
                active_ids=[booking.invoice_id.id]
            ).create({
                'amount': booking.invoice_id.amount_total,
                'payment_date': fields.Date.today(),
                'journal_id': self.env['account.journal'].search([('type', '=', 'bank')], limit=1).id,
            })

       
            payment_register.action_create_payments()

            booking.payment_state = 'paid'
 

               


    def create_invoice(self):
        for booking in self:
            if booking.invoice_id:
                raise UserError("Invoice already exists for this booking.")
            total = sum(line.amount_total for line in booking.room_line_ids)
            invoice=self.env['account.move'].create({
                    'move_type': 'out_invoice',
                    'partner_id': booking.partner_id.id,
                    'invoice_date': fields.Date.today(),
                    'invoice_origin': booking.name,
                    'hotel_booking_id':self.id ,
                    'invoice_line_ids': [(0, 0, {
                        'name': f"Booking {booking.room_line_ids.room_type_id.name}",
                        'quantity': booking.room_line_ids.quantity,
                        'price_unit': total,
                    })],
                })
            # invoice.action_post()
            booking.invoice_id = invoice.id
            booking.payment_state = 'invoiced'

            
            
    def action_send_email_wizard(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Send Booking Email',
            'res_model': 'send.email.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_booking_id': self.id,
            },
        }
        
        
        
    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('hotel.booking') or 'New'
        return super(HotelBooking, self).create(vals)    
        
        
        
        

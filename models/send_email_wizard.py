from odoo import models, fields, api
from odoo.exceptions import UserError


class SendEmailWizard(models.TransientModel):
    _name = 'send.email.wizard'
    _description = 'Send Booking Email Wizard'
    
    reciptent_id=fields.Many2one('res.partner',string="Customer")
    booking_id = fields.Many2one('hotel.booking', string='Booking')
    email_to = fields.Char(string="To", required=True)
    subject = fields.Char(string="Subject", required=True)
    body = fields.Text(string="Body", required=True)


    @api.model
    def default_get(self, fields_list):
        res = super(SendEmailWizard, self).default_get(fields_list)
        booking = self.env['hotel.booking'].browse(self.env.context.get('default_booking_id'))
        if booking:
            res.update({
                'reciptent_id': booking.partner_id.id,
                'email_to': booking.email or booking.partner_id.email,
                'subject': 'Hotel Booking Detail',
                'body': f"""
                    <p>Hello {booking.partner_id.name},</p>
                    <p>Thank You for Choosing our Hotel.</p>
                    <p>Your Hotel Booking is confirmed and number is <strong>{booking.name}</strong>.</p>
                    <p>Hotel and Room Details are attached in this mail.</p>
                    <br/>
                    <p>Regards,<br/>YourCompany</p>
                """
            })
        return res

    def send_email(self):
        if not self.email_to:
            raise UserError("Please enter a valid email address.")

        template = self.env.ref('hotel_management.booking_request_email_template')
        if not template:
            raise UserError("Email template 'booking_request_email_template' not found.")

        template.write({
            'email_to': self.email_to,
            'subject': self.subject,
            'body_html': self.body,
        })

        template.send_mail(self.booking_id.id, force_send=True)
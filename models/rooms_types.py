from odoo import models, fields,api
from odoo.exceptions import UserError, ValidationError
from datetime import date



class RoomsTypes(models.Model):
 
   _name = 'rooms.types'
   _description = 'Rooms Types'
   
   name=fields.Char(string='Name')
   charge=fields.Float(string='Charge')
   rooms_image=fields.Binary(string="Add")
   
   facilities = fields.Many2many('rooms.facility', string='Facilities')
   
    
   seasonable_price_ids = fields.One2many('hotel.seasonable.price', 'room_id', string="Seasonable Prices")



   _sql_constraints = [
        ('unique_name', 'unique(name)', 'Room type name must be unique.'),
    ]

   
#    @api.depends('seasonable_price_ids.start_date', 'seasonable_price_ids.end_date', 'seasonable_price_ids.price', 'seasonable_price_ids.active')
#    def _compute_price(self):
#         today = date.today()
#         for room in self:
#             seasonal_price = next(
#                 (sp.price for sp in room.seasonable_price_ids
#                  if sp.active and sp.start_date <= today <= sp.end_date),
#                 room.base_price
#             )
#             room.price = seasonal_price

   @api.constrains('charge')
   def _check_charge_positive(self):
        for record in self:
            if record.charge < 0:
                raise ValidationError(("Room charge must be a non-negative amount."))

   @api.constrains('name')
   def _check_name_not_blank(self):
        for record in self:
            if record.name and not record.name.strip():
                raise ValidationError(_("Room type name cannot be blank or only spaces."))
            
   @api.constrains('seasonable_price_ids')
   def _check_seasonable_prices(self):
        for record in self:
            for sp in record.seasonable_price_ids:
                if sp.start_date >= sp.end_date:
                    raise ValidationError(("Start date must be before end date in seasonable price."))


#    def action_generate_seasonable_price(self):
#         for hotel in self:
#             records = self.env['room.floor'].search([('hotel_id', '=', False)])
#             records.write({'hotel_id': hotel.id})
#         self.is_floor_generated = True

#    @api.model
#    def create(self, vals):
#         # import pdb;pdb.set_trace()
#         record = super(RoomsTypes, self).create(vals)

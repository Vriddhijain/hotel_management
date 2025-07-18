from odoo import models, fields


class PolicyTemplate(models.Model):
 
   _name = 'policy.template'
   _description = 'Policy Template'
   
   
   hotel_policy=fields.Char(string='Name')
   policy_details=fields.Text(string='Policy Details')
   # policy_template_ids=fields.Many2one('hotel.booking', string='Policy')
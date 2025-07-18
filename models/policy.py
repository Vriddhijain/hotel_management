from odoo import models, fields


class Policy(models.Model):
 
   _name = 'policy'
   _description = 'Policy'
   
   
   name = fields.Char(string='Policy Name', required=True)
   policy_template_id = fields.Many2one('policy.template', string='Policy Template')
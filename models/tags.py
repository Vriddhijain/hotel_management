from odoo import models, fields


class TagsAmeneities(models.Model):
 
   _name = 'tags'
   _description = 'Tags'
   
   tag_name=fields.Char(string='Name')

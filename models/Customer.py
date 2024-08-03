from odoo import models, fields,api

class Customer(models.Model):
    _inherit = 'res.partner'


    phone = fields.Char(string="Phone Number", required=True)
    email = fields.Char(string="Email")
    cin = fields.Char(string="CIN Number")






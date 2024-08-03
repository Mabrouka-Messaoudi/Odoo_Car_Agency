from odoo import models, fields, api,_


class CarBrand(models.Model):
    _name = "car_agency.car_brand"
    _description = 'CarBrand'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(String="name",required=True,default=lambda self:_('New'),tracking=1)
    image = fields.Binary(String="image")
    description = fields.Char(String="description")

    agency_id = fields.Many2one('car_agency.agency', String='agency', required=True)




    @api.model
    def create(self, vals):
        """to create sequence number for the brand"""
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('car_agency.car_brand.sequence') or _('New')
        result = super(CarBrand, self).create(vals)
        return result


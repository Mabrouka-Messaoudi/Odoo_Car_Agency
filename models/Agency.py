from odoo import models, fields,api

class Agency(models.Model):
    _name = 'car_agency.agency'
    _description = 'Car Agency'
    _rec_name = 'agency'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    agency = fields.Char(string="agency")
    responsible_person = fields.Many2one('res.partner', string='Responsible Person', required=True)
    agency_list_brand=fields.One2many('car_agency.car_brand','agency_id',String="CarBrand",readonly=True)
    agency_list_cars=fields.One2many('car_agency.car','agency_id',String='Cars',tracking=1)
    tag_ids=fields.Many2many('res.partner.category','agency_tags','agency_id','tag_id',string="Tags")
    phone=fields.Char(string="phone")


    def action_view_brands(self):
        """display the brands list smart button action"""
        action = self.env.ref('car_agency.action_car_brand').read()[0]
        action['domain'] = [('agency_id', '=', self.id)]
        return action


    @api.onchange('responsible_person')
    def onchange_responsible_person(self):
        """ it changes automatically the phone number when the responsible person changes"""
        if self.responsible_person:
            if self.responsible_person.phone:
                self.phone = self.responsible_person.phone
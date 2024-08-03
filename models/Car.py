from odoo import models, fields, api, _
from datetime import datetime
from odoo.exceptions import ValidationError


class Car(models.Model):
    _name = "car_agency.car"
    _description = "Car"
    _rec_name = 'model'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    registration_number = fields.Integer(string="Registration Number", required=True, index=True)
    model = fields.Char(string="Model", required=True)
    mileage = fields.Float(string="Mileage")
    state = fields.Selection([
        ('available', 'Available'),
        ('rented', 'Rented'),
        ('damaged', 'Damaged')
    ], default='available',string="state")

    startdate = fields.Date(string="Date of Start")
    enddate = fields.Date(string="Date of End")
    agency_id = fields.Many2one('car_agency.agency', string='Agency')
    brand_id = fields.Many2one('car_agency.car_brand', string='Brand')
    note = fields.Text(string="Note")
    duration_of_rent = fields.Integer(string='Duration of rent', compute='_compute_rent')

    def action_open_damage_wizard(self):
        """ open a wizard for defining the reason of damage"""

        return {
            'name': 'Damage Car',
            'type': 'ir.actions.act_window',
            'res_model': 'car.damage.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_note': self.note},
        }

    def action_available(self):
        """ click on the button and change the state """
        self.state = 'available'

    def action_rented(self):
        """ click on the button and change the state """
        self.state = 'rented'


    _sql_constraints = [
        ('registration_number', 'unique(registration_number)', "The registration number is unique for each car!"),
        ('eight_digits_number', 'CHECK(length(str(registration_number)) = 8)',
         "The registration number must contains 8 digits")
    ]

    @api.constrains('registration_number')
    def _check_registration(self):
        """ verify that registration number contains 8 digits and positive """
        for record in self:
            if record.registration_number < 0:
                raise ValidationError('The registration number must be positive')
            elif len(str(record.registration_number)) != 8:
                raise ValidationError('The registration number must containt 8 digits')



    @api.depends('startdate', 'enddate')
    def _compute_rent(self):
        """ calculate the duration of rent"""
        for rec in self:
            rec.duration_of_rent = False
            if rec.startdate and rec.enddate:
                start_date = fields.Date.from_string(rec.startdate)
                end_date = fields.Date.from_string(rec.enddate)
                delta = end_date - start_date
                rec.duration_of_rent = delta.days



    def action_view_requests(self):
        """display the brands list"""
        action = self.env.ref('car_agency.action_request').read()[0]
        action['domain'] = [('car', '=', self.id)]
        return action


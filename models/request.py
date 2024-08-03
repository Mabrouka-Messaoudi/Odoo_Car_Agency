import logging
from datetime import date

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError


class Request(models.Model):
    _name = "car_agency.request"
    _description = "Request"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="request", default=lambda self: _('New'))
    car = fields.Many2one('car_agency.car', string="car")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('send', 'Sent To Responsible'),
        ('cancel', 'Canceled'),
        ('confirm', 'Confirmed'),
        ('refuse', 'refused'),
    ], string="state", default='draft')
    start_date = fields.Date(string="Date of Start")
    end_date = fields.Date(string="Date of End")
    responsible_person = fields.Char(string="Manager", related='car.agency_id.responsible_person.name', store=True)
    agency = fields.Char(string="agency", related='car.agency_id.agency', store=True)
    renter_id=fields.Many2one('res.partner',String='renter')

    """@api.constrains('start_dat','end_date','car')
    def _check_dates(self):
         check if the car is available
        for record in self:
            if record.car.startdate and record.car.enddate:

                car_start_date = record.car.startdate
                car_end_date= record.car.enddate
                request_start_date = record.end_date
                request_end_date=record.end_date
                if request_start_date >= car_start_date or request_end_date <= car_end_date:
                    raise ValidationError("car is not available")"""

    def action_cancel(self):
        """ click on the button and change the state """
        self.state = 'cancel'

    def action_confirm(self):
        """ click on the button and change the state """

        self.car.state = 'rented'
        self.car.startdate = self.start_date
        self.car.enddate = self.end_date
        self.state = 'confirm'
        self.send_confirmation_email()


    def action_send(self):
        """click on the button and change the state"""
        self.state = 'send'


    def action_refuse(self):
        """click on the button and change the state"""
        self.state = 'refuse'

    @api.constrains('start_date', 'end_date')
    def _check_validation_date(self):
        """ "verify that the date of start is  lower than the date of end """
        for record in self:
            if record.start_date > record.end_date and record.end_date > date.today():
                raise ValidationError('the date of start must be lower than the date of end')


    @api.model
    def create(self, vals):
        """ to create a sequence number for  the request """
        if vals.get('name', _('New')) == _('New'):
            seq = self.env['ir.sequence'].next_by_code('car_agency.request') or _('New')
            vals['name'] = seq
        result = super(Request, self).create(vals)
        return result
    @api.model
    def _check_car_rental_status(self):
        """cron to check the car state """
        today = date.today()
        requests = self.search([('state', '=', 'confirm'), ('end_date', '<', today)])
        for request in requests:
            request.car.state = 'available'

            request.car.startdate = False
            request.car.enddate = False

        requests = self.search([('state', '=', 'confirm'), ('start_date', '<=', today), ('end_date', '>=', today)])
        for request in requests:
            request.car.state = 'rented'

            request.car.startdate = request.start_date
            request.car.enddate = request.end_date


    def send_confirmation_email(self):
        """send a confirmation mail to the request sender """
        template = self.env.ref('car_agency.rental_mail_template')
        for rec in self:
            template.send_mail(rec.id,force_send=True)


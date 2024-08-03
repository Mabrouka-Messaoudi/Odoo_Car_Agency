from odoo import models, fields, api

class CarDamageWizard(models.TransientModel):
    _name = 'car.damage.wizard'

    note = fields.Text(string='Description for Cause of Damage')

    def action_save_damage_note(self):
        """action for the save button """
        active_id = self.env.context.get('active_id')
        car = self.env['car_agency.car'].browse(active_id)
        car.write({
            'note': self.note,
            'state': 'damaged',
        })
        return {'type': 'ir.actions.act_window_close'}
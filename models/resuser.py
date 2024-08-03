from odoo import models, api

class ResUsers(models.Model):
    _inherit = 'res.users'

    def action_view_rental_requests(self):
        """action for the button smart button  """
        self.ensure_one()
        return {
            'name': 'Rental Requests',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': 'car_agency.request',
            'domain': [('responsible_person', '=', self.partner_id.name)],
            'context': dict(self._context, create=False),
        }
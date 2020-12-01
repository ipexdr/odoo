from odoo import api, models, fields


class User(models.Model):
    _inherit = ['res.users']

    hand_signature = fields.Image('Handwritten Signature', max_height=350, max_width=200)
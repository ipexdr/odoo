# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)

#TODO: Set translations

class AccountPayment(models.Model):
    _inherit = "account.payment"
        
    @api.onchange('amount', 'currency_id')
    def _onchange_amount(self):
        res = super(AccountPayment, self)._onchange_amount()
        
        check_amount_in_words = self.currency_id.amount_to_text(float(int(self.amount))) if self.currency_id else ''
        
        if check_amount_in_words:
            if self.amount.is_integer():
                cents = _(' con ') + '0/100'
            else:
                cent = str(self.amount).split('.')[1].ljust(2, '0')[:2]
                cents = _(' con ') + f'{cent}/100'
            self.check_amount_in_words = check_amount_in_words + cents
        else:
            self.check_amount_in_words = check_amount_in_words
        
        return res
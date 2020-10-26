# -*- coding: utf-8 -*-
from odoo.tests import TransactionCase, tagged, Form

@tagged('ncf', 'post_install', '-at_install')
class TestAccountMoveNCF(TransactionCase):
    def setUp(self):
        super(TestAccountMoveNCF, self).setUp()
        self.account_move = Form(self.env['account.move'])
    
    # TODO: Test when move is saved/created
    
    # TODO: ??? Test when input used NCF
        
    def test_correct_ncf_onchange(self):
        '''
        Testing if the NCF is the right one after triggering onchange on ncf_type
        '''
        
        self.account_move.ncf_type = 'ncf.gasto.menor'
        sequence = self.env['ir.sequence'].search([('code','=',self.account_move.ncf_type)])
        ncf = sequence.get_next_char(sequence.number_next_actual)
        self.assertEqual(self.account_move.ncf, ncf)
        
        self.account_move.ncf_type = 'ncf.con.final'
        sequence = self.env['ir.sequence'].search([('code','=',self.account_move.ncf_type)])
        ncf = sequence.get_next_char(sequence.number_next_actual)
        self.assertEqual(self.account_move.ncf, ncf)
        
        self.account_move.ncf_type = 'ncf.reg.especial'
        sequence = self.env['ir.sequence'].search([('code','=',self.account_move.ncf_type)])
        ncf = sequence.get_next_char(sequence.number_next_actual)
        self.assertEqual(self.account_move.ncf, ncf)
        
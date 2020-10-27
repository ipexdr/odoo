# -*- coding: utf-8 -*-
from odoo.tests import TransactionCase, tagged, Form
from odoo.exceptions import ValidationError
from odoo.addons.account.tests.account_test_savepoint import AccountTestInvoicingCommon

@tagged('ncf', 'post_install', '-at_install')
class TestAccountMoveNCF(TransactionCase):
    def setUp(self):
        super(TestAccountMoveNCF, self).setUp()
        self.account_move = self.env['account.move']
    
    def test_ncf_char_min_length(self):
        '''Ensure form raises ValidationError exc if ncf length is lesser than 11 char'''
        account_move_form = Form(self.account_move)
            
        with self.assertRaises(ValidationError):
            account_move_form.ncf = 'XXXXXXXXXX'
            account_move_form.save()
            
    def test_ncf_char_max_length(self):
        '''Ensure the length of the NCF is equals to 11 even if it is given more characters, after been saved'''
        form = Form(self.account_move)
        form.ncf = 'XXXXXXXXXXXXX'
        form.save()
        self.assertEqual(len(form.ncf), 11)
        
    def test_auto_ncf_save_sequence(self):
        '''Ensure that NCF is saved and next one is generated correctly afterwards (when assigned automatically)
        -Assuming ncf.gasto.menor sequence parameters:
        --Prefix	      B13
        --Sequence Size	  8
        --Step	          1
        --Next Number	  3
        '''
        
        form1 = Form(self.account_move)
        form1.ncf_type = 'ncf.gasto.menor'    
        form1.save()
        self.assertEqual(form1.ncf, 'B1300000001')
        
        form2 = Form(self.account_move)
        form2.ncf_type = 'ncf.gasto.menor'
        form2.save()
        self.assertEqual(form2.ncf, 'B1300000002')
        
        form3 = Form(self.account_move)
        form3.ncf_type = 'ncf.gasto.menor'
        form3.save()
        self.assertEqual(form3.ncf, 'B1300000003')
        
        
    # TODO: Test when move is saved/created
    
    # TODO: ??? Test when input used NCF
        
    def test_form_ncf_onchange(self):
        '''
        Testing if the NCF is the right one after triggering onchange on ncf_type
        '''
        
        self.account_move_form = Form(self.env['account.move'])
        
        
        self.account_move_form.ncf_type = 'ncf.gasto.menor'
        sequence = self.env['ir.sequence'].search([('code','=',self.account_move_form.ncf_type)])
        ncf = sequence.get_next_char(sequence.number_next_actual)
        self.assertEqual(self.account_move_form.ncf, ncf)
        
        self.account_move_form.ncf_type = 'ncf.con.final'
        sequence = self.env['ir.sequence'].search([('code','=',self.account_move_form.ncf_type)])
        ncf = sequence.get_next_char(sequence.number_next_actual)
        self.assertEqual(self.account_move_form.ncf, ncf)
        
        self.account_move_form.ncf_type = 'ncf.reg.especial'
        sequence = self.env['ir.sequence'].search([('code','=',self.account_move_form.ncf_type)])
        ncf = sequence.get_next_char(sequence.number_next_actual)
        self.assertEqual(self.account_move_form.ncf, ncf)
        
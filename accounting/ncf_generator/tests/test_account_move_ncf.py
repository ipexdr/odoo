# -*- coding: utf-8 -*-
from odoo.addons.account.tests.account_test_savepoint import AccountTestInvoicingCommon
from odoo.tests import TransactionCase, tagged, Form
from odoo.exceptions import ValidationError
from odoo import fields
import logging

_logger = logging.getLogger(__name__)

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
        '''Ensure the length of the NCF is equals to 11 even if it is given more characters, after saved'''
        form = Form(self.account_move)
        form.ncf = 'XXXXXXXXXXXXX'
        form.save()
        self.assertEqual(len(form.ncf), 11)
        
    def test_auto_ncf_save_sequence(self):
        '''Ensure that NCF is saved and next one is generated correctly afterwards (when assigned automatically)

        -Assuming gasto.menor sequence parameters:
        --Prefix	      B13
        --Sequence Size	  8
        --Step	          1
        --Next Number	  3
        '''
        
        form1 = Form(self.account_move)
        form1.ncf_type = self.env['ir.sequence'].search([('is_ncf','=',True)])[0]
        sequence = self.env['ir.sequence'].next_by_code(form1.ncf_type.code)
        form1.save()
        self.assertEqual(form1.ncf, sequence)
        
        form2 = Form(self.account_move)
        form2.ncf_type = self.env['ir.sequence'].search([('is_ncf','=',True)])[0]
        sequence = self.env['ir.sequence'].next_by_code(form2.ncf_type.code)
        form2.save()
        self.assertEqual(form2.ncf, sequence)
        
        form3 = Form(self.account_move)
        form3.ncf_type = self.env['ir.sequence'].search([('is_ncf','=',True)])[0]
        sequence = self.env['ir.sequence'].next_by_code(form3.ncf_type.code)
        form3.save()
        self.assertEqual(form3.ncf, sequence)
        
    def test_unique_ncf(self):
        '''Ensure an exception is raised if a NCF is already taken'''
        
        form1 = Form(self.account_move)
        form1.ncf_type = self.env['ir.sequence'].search([('is_ncf','=',True)])[0]
        form1.save()
        
        form2 = Form(self.account_move)
        form2.ncf = form1.ncf
        
        with self.assertRaises(ValidationError):
            form2.save()
            
        
    def test_form_ncf_onchange(self):
        '''
        Testing if the NCF is the right one after triggering onchange on ncf_type
        '''
        
        self.account_move_form = Form(self.env['account.move'])
        
        self.account_move_form.ncf_type = self.env['ir.sequence'].search([('is_ncf','=',True)])[0]
        sequence = self.env['ir.sequence'].search([('code','=',self.account_move_form.ncf_type.code)])
        ncf = sequence.get_next_char(sequence.number_next_actual)
        self.assertEqual(self.account_move_form.ncf, ncf)
        
        self.account_move_form.ncf_type = self.env['ir.sequence'].search([('is_ncf','=',True)])[1]
        sequence = self.env['ir.sequence'].search([('code','=',self.account_move_form.ncf_type.code)])
        ncf = sequence.get_next_char(sequence.number_next_actual)
        self.assertEqual(self.account_move_form.ncf, ncf)
        
        self.account_move_form.ncf_type = self.env['ir.sequence'].search([('is_ncf','=',True)])[2]
        sequence = self.env['ir.sequence'].search([('code','=',self.account_move_form.ncf_type.code)])
        ncf = sequence.get_next_char(sequence.number_next_actual)
        self.assertEqual(self.account_move_form.ncf, ncf)
        
    def test_ncf_sequence_create(self):
        '''Try to create a ncf_sequence object.'''
        
        ncf_seq = self.env['ir.sequence'].create({
            'code':'test.ncf.sequence',
            'name':'test ncf'
        })
        self.assertTrue(ncf_seq)

    # account.move.type will be used to know which ncf sequences will be available.

        # selection=[
        #     ('entry', 'Journal Entry'),
        #     ('out_invoice', 'Customer Invoice'),
        #     ('out_refund', 'Customer Credit Note'),
        #     ('in_invoice', 'Vendor Bill'),
        #     ('in_refund', 'Vendor Credit Note'),
        #     ('out_receipt', 'Sales Receipt'),
        #     ('in_receipt', 'Purchase Receipt'),
        # ]


    # if move type is in ncf_sequence, the ncf_sequence must be able to be selected and
    # saved in an account_move of that type
    def test_move_type_in_ncf_sequence(self):
        
        form = Form(self.account_move)
        form.save()
        
        move_types = []
        move_types.append(self.env['ncf_generator.move_type'].search([('code','=',form.type)]).id)
        
        ncf_seq = self.env['ir.sequence'].create({
            'code':'test.ncf.seq',
            'name':'test ncf',
            'move_type_ids': move_types,
            'padding': 8,
            'number_increment': 1,
            'prefix':'XXX',
            'is_ncf': True
        })
        ncf = ncf_seq.get_next_char(ncf_seq.number_next_actual)
        
        form.ncf_type = ncf_seq
        form.save()
        self.assertEqual(ncf, form.ncf)
        
    # if move type is no in ncf_sequence, can't be selected in account_move
    def test_move_type_not_in_ncf_sequence(self):
        form = Form(self.account_move)
        form.save()
        
        move_types = []
        move_types.extend(move_type.id for move_type in self.env['ncf_generator.move_type'].search([('code','!=',form.type)]))
        
        ncf_seq = self.env['ir.sequence'].create({
            'code':'test.ncf.seq',
            'name':'test ncf',
            'move_type_ids': move_types,
            'padding': 8,
            'number_increment': 1,
            'prefix':'XXX',
            'is_ncf': True
        })

        with self.assertRaises(ValidationError):
            # Raise when move type isn't in ncf sequence
            form.ncf_type = ncf_seq
            form.save()

@tagged('post_install', '-at_install')
class TestAccountMoveInInvoiceOnchanges(AccountTestInvoicingCommon):

    @classmethod
    def setUpClass(cls, chart_template_ref=None):
        super().setUpClass(chart_template_ref=chart_template_ref)

        cls.invoice = cls.init_invoice('in_invoice')

        cls.product_line_vals_1 = {
            'name': cls.product_a.name,
            'product_id': cls.product_a.id,
            'account_id': cls.product_a.property_account_expense_id.id,
            'partner_id': cls.partner_a.id,
            'product_uom_id': cls.product_a.uom_id.id,
            'quantity': 1.0,
            'discount': 0.0,
            'price_unit': 800.0,
            'price_subtotal': 800.0,
            'price_total': 920.0,
            'tax_ids': cls.product_a.supplier_taxes_id.ids,
            'tax_line_id': False,
            'currency_id': False,
            'amount_currency': 0.0,
            'debit': 800.0,
            'credit': 0.0,
            'date_maturity': False,
            'tax_exigible': True,
        }
        cls.product_line_vals_2 = {
            'name': cls.product_b.name,
            'product_id': cls.product_b.id,
            'account_id': cls.product_b.property_account_expense_id.id,
            'partner_id': cls.partner_a.id,
            'product_uom_id': cls.product_b.uom_id.id,
            'quantity': 1.0,
            'discount': 0.0,
            'price_unit': 160.0,
            'price_subtotal': 160.0,
            'price_total': 208.0,
            'tax_ids': cls.product_b.supplier_taxes_id.ids,
            'tax_line_id': False,
            'currency_id': False,
            'amount_currency': 0.0,
            'debit': 160.0,
            'credit': 0.0,
            'date_maturity': False,
            'tax_exigible': True,
        }
        cls.tax_line_vals_1 = {
            'name': cls.tax_purchase_a.name,
            'product_id': False,
            'account_id': cls.company_data['default_account_tax_purchase'].id,
            'partner_id': cls.partner_a.id,
            'product_uom_id': False,
            'quantity': 1.0,
            'discount': 0.0,
            'price_unit': 144.0,
            'price_subtotal': 144.0,
            'price_total': 144.0,
            'tax_ids': [],
            'tax_line_id': cls.tax_purchase_a.id,
            'currency_id': False,
            'amount_currency': 0.0,
            'debit': 144.0,
            'credit': 0.0,
            'date_maturity': False,
            'tax_exigible': True,
        }
        cls.tax_line_vals_2 = {
            'name': cls.tax_purchase_b.name,
            'product_id': False,
            'account_id': cls.company_data['default_account_tax_purchase'].id,
            'partner_id': cls.partner_a.id,
            'product_uom_id': False,
            'quantity': 1.0,
            'discount': 0.0,
            'price_unit': 24.0,
            'price_subtotal': 24.0,
            'price_total': 24.0,
            'tax_ids': [],
            'tax_line_id': cls.tax_purchase_b.id,
            'currency_id': False,
            'amount_currency': 0.0,
            'debit': 24.0,
            'credit': 0.0,
            'date_maturity': False,
            'tax_exigible': True,
        }
        cls.term_line_vals_1 = {
            'name': '',
            'product_id': False,
            'account_id': cls.company_data['default_account_payable'].id,
            'partner_id': cls.partner_a.id,
            'product_uom_id': False,
            'quantity': 1.0,
            'discount': 0.0,
            'price_unit': -1128.0,
            'price_subtotal': -1128.0,
            'price_total': -1128.0,
            'tax_ids': [],
            'tax_line_id': False,
            'currency_id': False,
            'amount_currency': 0.0,
            'debit': 0.0,
            'credit': 1128.0,
            'date_maturity': fields.Date.from_string('2019-01-01'),
            'tax_exigible': True,
        }
        cls.move_vals = {
            'partner_id': cls.partner_a.id,
            'currency_id': cls.company_data['currency'].id,
            'journal_id': cls.company_data['default_journal_purchase'].id,
            'date': fields.Date.from_string('2019-01-01'),
            'fiscal_position_id': False,
            'invoice_payment_ref': '',
            'invoice_payment_term_id': cls.pay_terms_a.id,
            'amount_untaxed': 960.0,
            'amount_tax': 168.0,
            'amount_total': 1128.0,
        }

    def setUp(self):
        super(TestAccountMoveInInvoiceOnchanges, self).setUp()
        self.assertInvoiceValues(self.invoice, [
            self.product_line_vals_1,
            self.product_line_vals_2,
            self.tax_line_vals_1,
            self.tax_line_vals_2,
            self.term_line_vals_1,
        ], self.move_vals)
        
    def test_reversal_from_invoice(self):
        '''Test credit note creation from an invoice with ncf.
        Reversal must have the invoice ncf in mod_ncf field'''
        
        inv_form = Form(self.invoice)
#         inv_form = Form(self.env['account.move'].with_context(default_type='in_invoice'))
        inv_form.partner_id = self.partner_a
        inv_form.ncf = "XXXXXXXXXXX"
        inv = inv_form.save()
        inv.post()
        
        move_reversal = self.env['account.move.reversal'].with_context(active_model="account.move", active_ids=inv.ids).create({
            'date': fields.Date.from_string('2019-02-01'),
            'reason': 'no reason',
            'refund_method': 'refund',
        })
        reversal = move_reversal.reverse_moves()
        reverse_move = self.env['account.move'].browse(reversal['res_id'])
        self.assertEquals((inv.ncf, inv.id), (reversal_move.mod_ncf, reversal_move.parent_move_id))
        
        
        
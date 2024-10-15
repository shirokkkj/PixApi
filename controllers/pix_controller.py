from flask import Blueprint, render_template, session
from entry_forms.forms import PixForm
from models.db_models import User, Transactions
import uuid
from utils.utils import update_user_balance, encrypt_data
from config import redis_connection
import datetime
import json

pix_controller = Blueprint('pix_controller', __name__)

@pix_controller.route('/pix-secret_key')
def pix_secret_key():
    form = PixForm()
    # This route is made solely to render the pix submission form.
    return render_template('make_secretkey_pix.html', form=form)

@pix_controller.route('/make-secret_key-pix', methods=['POST'])
def make_secretkey_pix():
    form = PixForm()
    
    '''
    Here is the first Endpoint written, designed to actually perform transactions. Responsible for taking the information sent from the form, validating it and thus making the transaction a success. There are validations already done in the **make_transaction** method, so only form validations appear here.
    
    To see how the method used is written, go to models/db_models
    '''
    
    if form.validate_on_submit():
        transation = User.make_transaction_by_secretkey(session.get('user_id'), form.pix_key.data, form.amount.data)
        payer = User.find_by_id(session.get('user_id'))
        payee = User.find_by_secret_key(form.pix_key.data)
        
        if transation['status'] == 'success':
            transaction_id = str(uuid.uuid4())
            Transactions.make_transation(session.get('user_id'), payer.name, payee.id, payee.name, transaction_id, form.amount.data)
            
            update_user_balance(redis_connection, session.get('user_id'), form.amount.data, True) # Update cache of PAYER
            
            update_user_balance(redis_connection, payee.id, form.amount.data, False)
            
            return render_template('comprovante.html', 
                                   secret_key=form.pix_key.data, 
                                   amount=form.amount.data, 
                                   payer=payer.name, 
                                   payee=payee.name, 
                                   weekday=datetime.datetime.today().strftime('%A'), 
                                   date=datetime.date.today(), 
                                   hour=datetime.datetime.now().strftime('%H:%M:%S'), 
                                   transaction_id=transaction_id)
        else:
            return render_template('error_transaction.html', error_message=transation['reason'])
    return transation


@pix_controller.route('/pix-cpf')
def pix_cpf():
    form = PixForm()

    return render_template('make_cpf_pix.html', form=form)

@pix_controller.route('/make-cpf-pix', methods=['POST'])
def make_cpf_pix():
    form = PixForm()
    
    
    if form.validate_on_submit():
        transation = User.make_transaction_by_cpf(session.get('user_id'), form.pix_key.data, form.amount.data)
        payer = User.find_by_id(session.get('user_id'))
        payee = User.find_by_cpf(encrypt_data(form.pix_key.data))
        
        if transation['status'] == 'success':
            transaction_id = str(uuid.uuid4())
            Transactions.make_transation(session.get('user_id'), payer.name, payee.id, payee.name, transaction_id, form.amount.data)
            
            update_user_balance(redis_connection, session.get('user_id'), form.amount.data, True) # Update cache of PAYER
            
            update_user_balance(redis_connection, payee.id, form.amount.data, False)
            
            return render_template('comprovante.html', 
                                   pix_key=form.pix_key.data, 
                                   amount=form.amount.data, 
                                   payer=payer.name, 
                                   payee=payee.name, 
                                   weekday=datetime.datetime.today().strftime('%A'), 
                                   date=datetime.date.today(), 
                                   hour=datetime.datetime.now().strftime('%H:%M:%S'), 
                                   transaction_id=transaction_id)
        else:
            return render_template('error_transaction.html', error_message=transation['reason'])    
    return transation


@pix_controller.route('/pix-email')
def pix_email():
    form = PixForm()

    return render_template('make_email_pix.html', form=form)

@pix_controller.route('/make-email-pix', methods=['POST'])
def make_email_pix():
    form = PixForm()
    
    
    if form.validate_on_submit():
        transation = User.make_transaction_by_email(session.get('user_id'), form.pix_key.data, form.amount.data)
        payer = User.find_by_id(session.get('user_id'))
        payee = User.find_by_email(encrypt_data(form.pix_key.data))
        
        if transation['status'] == 'success':
            transaction_id = str(uuid.uuid4())
            Transactions.make_transation(session.get('user_id'), payer.name, payee.id, payee.name, transaction_id, form.amount.data)
            
            update_user_balance(redis_connection, session.get('user_id'), form.amount.data, True) # Update cache of PAYER
            
            update_user_balance(redis_connection, payee.id, form.amount.data, False)
            
            return render_template('comprovante.html', 
                                   pix_key=form.pix_key.data, 
                                   amount=form.amount.data, 
                                   payer=payer.name, 
                                   payee=payee.name, 
                                   weekday=datetime.datetime.today().strftime('%A'), 
                                   date=datetime.date.today(), 
                                   hour=datetime.datetime.now().strftime('%H:%M:%S'), 
                                   transaction_id=transaction_id)
        else:
            return render_template('error_transaction.html', error_message=transation['reason'])
    return transation


@pix_controller.route('/pix-phone')
def pix_phone():
    form = PixForm()

    return render_template('make_phone_pix.html', form=form)

@pix_controller.route('/make-phone-pix', methods=['POST'])
def make_phone_pix():
    form = PixForm()
    
    
    if form.validate_on_submit():
        print(encrypt_data(form.pix_key.data))
        transation = User.make_transaction_by_phone(session.get('user_id'), form.pix_key.data, form.amount.data)
        payer = User.find_by_id(session.get('user_id'))
        payee = User.find_by_phone(encrypt_data(form.pix_key.data))
        
        if transation['status'] == 'success':
            transaction_id = str(uuid.uuid4())
            Transactions.make_transation(session.get('user_id'), payer.name, payee.id, payee.name, transaction_id, form.amount.data)
            
            update_user_balance(redis_connection, session.get('user_id'), form.amount.data, True) # Update cache of PAYER
            
            update_user_balance(redis_connection, payee.id, form.amount.data, False)
            
            return render_template('comprovante.html', 
                                   pix_key=form.pix_key.data, 
                                   amount=form.amount.data, 
                                   payer=payer.name, 
                                   payee=payee.name, 
                                   weekday=datetime.datetime.today().strftime('%A'), 
                                   date=datetime.date.today(), 
                                   hour=datetime.datetime.now().strftime('%H:%M:%S'), 
                                   transaction_id=transaction_id)
        else:
            return render_template('error_transaction.html', error_message=transation['reason'])
    return transation
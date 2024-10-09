from flask import Blueprint, render_template, session
from models.db_models import User, Transactions
from entry_forms.forms import PixForm, TransactionDateSearch
import datetime
import uuid
from config import redis_connection
import json
from utils.utils import update_user_balance


home_controller = Blueprint('home_controller', __name__) # ''home_controller'' is just to organize the main routes and endpoints of our project.

@home_controller.route('/')
def home():
    
    '''
    The main route, that is, the / route, is responsible for showing the user how much money they have in their account, as well as welcoming them with their name. That's why we get this information using the methods of the user class.
    
    
    To find the methods used, go to the directory models/db_models
    '''
    user_id = session.get("user_id")
    value = f"user:{user_id}"

    user = redis_connection.get(value).decode('utf-8')
    loaded_data = json.loads(user)
    
    print(user)

    
    balance = loaded_data['balance']
    name = loaded_data['name']
    
    return render_template('home.html', balance=balance, name=name)

@home_controller.route('/pix-form')
def pix_form():
    form = PixForm()
    # This route is made solely to render the pix submission form.
    return render_template('make_pix.html', form=form)

@home_controller.route('/make-pix', methods=['POST'])
def make_pix():
    form = PixForm()
    
    '''
    Here is the first Endpoint written, designed to actually perform transactions. Responsible for taking the information sent from the form, validating it and thus making the transaction a success. There are validations already done in the **make_transaction** method, so only form validations appear here.
    
    To see how the method used is written, go to models/db_models
    '''
    
    if form.validate_on_submit():
        transation = User.make_transaction(session.get('user_id'), form.secret_key.data, form.amount.data)
        payer = User.find_by_id(session.get('user_id'))
        payee = User.find_by_secret_key(form.secret_key.data)
        
        if transation['status'] == 'success':
            transaction_id = str(uuid.uuid4())
            Transactions.make_transation(session.get('user_id'), payer.name, payee.id, payee.name, transaction_id, form.amount.data)
            
            update_user_balance(redis_connection, session.get('user_id'), form.amount.data, True) # Update cache of PAYER
            
            update_user_balance(redis_connection, payee.id, form.amount.data, False)
            
            return render_template('comprovante.html', 
                                   secret_key=form.secret_key.data, 
                                   amount=form.amount.data, 
                                   payer=payer.name, 
                                   payee=payee.name, 
                                   weekday=datetime.datetime.today().strftime('%A'), 
                                   date=datetime.date.today(), 
                                   hour=datetime.datetime.now().strftime('%H:%M:%S'), 
                                   transaction_id=transaction_id)
    return transation

@home_controller.route('/payment-transactions', methods=['GET', 'POST'])
def payment_transactions():
    form = TransactionDateSearch()
    transations = Transactions.get_payment_transactions(session.get('user_id'))
    
    if form.validate_on_submit():
        parsed_date = datetime.datetime.strptime(str(form.date.data), '%Y-%m-%d')
        transations = Transactions.get_transactions_by_date(parsed_date)
    
    return render_template('payment_transactions.html', transations=transations, form=form)

@home_controller.route('/recebment-transactions', methods=['GET', 'POST'])
def recebment_transactions():
    form = TransactionDateSearch()
    transations = Transactions.get_recebment_transactions(session.get('user_id'))
    
    if form.validate_on_submit():
        parsed_date = datetime.datetime.strptime(str(form.date.data), '%Y-%m-%d')
        transations = Transactions.get_transactions_by_date(parsed_date)
    
    return render_template('recebment_transactions.html', transations=transations, form=form)

@home_controller.route('/create_pix_key')
def create_pix_key():
    return render_template('create_pix_key.html')

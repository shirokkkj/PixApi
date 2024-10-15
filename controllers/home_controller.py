from flask import Blueprint, render_template, session, request
from models.db_models import User, Transactions
from entry_forms.forms import PixForm, TransactionDateSearch
import datetime
import uuid
from config import redis_connection
import json
from utils.utils import update_user_balance
from socketio_configs import send_notification


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


@home_controller.route('/socket-emit')
def socket_emit_route():
    send_notification(session.get('user_id'), {'message': 'ola'})
    


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

@home_controller.route('/select-pix-form')
def select_pix_form():
    return render_template('select_pix.html')

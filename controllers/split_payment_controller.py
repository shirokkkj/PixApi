from flask import Blueprint, render_template, session, jsonify, redirect, url_for
from models.db_models import User, Transactions
from utils.utils import uncrypt_data, hash_password, check_password
from entry_forms.forms import PasswordConfirmForm, PixForm, SplitPaymentForm
import bcrypt
from config import db
from config import redis_connection
from socketio_configs import send_notification
from utils.utils import encrypt_data
import uuid
from time import sleep

split_payment_controller = Blueprint('split_payment_controller', __name__)

@split_payment_controller.route('/split-payment-form')
def split_payment_form():
    form = SplitPaymentForm()
    
    return render_template('split_payment_form.html', form=form)


@split_payment_controller.route('/make-split-payment', methods=['POST'])
def make_split_payment():
    form = SplitPaymentForm()
    
    if form.validate_on_submit():
        payee = User.find_by_cpf(encrypt_data(form.pix_key.data))
        id_transaction = str(uuid.uuid4())
        
        payer = User.find_by_id(session.get('user_id'))
        transaction = Transactions.make_transation(payer.id, payer.name, payee.id, payee.name, id_transaction=id_transaction,amount=form.amount.data, type='Split')
        send_notification(payee.id, payer.name, transaction.id, payer.id, form.pix_key.data, form.receiver_key.data,float(form.amount.data) )
    
        return render_template('await_transaction.html')
from flask import Blueprint, render_template, session, jsonify, redirect, url_for
from models.db_models import User
from utils.utils import uncrypt_data, hash_password, check_password
from entry_forms.forms import PasswordConfirmForm
import bcrypt
from config import db
from config import redis_connection
from socketio_configs import send_notification

pix_keys_controller = Blueprint('pix_keys_controller', __name__)

@pix_keys_controller.route('/cpf-key-form')
def cpf_key_form():
    form = PasswordConfirmForm()
    user_data = User.find_by_id(session.get('user_id'))
    cpf = user_data.cpf
    registered = False
    title = False
    paragraph = False
    
    if user_data.registered_phone_key:
        title = 'Você já tem uma chave pix registrada.'
        paragraph = 'Sua chave pix'
        registered = True
    
    uncrypted_cpf = uncrypt_data(cpf)
    parsed_cpf = '{}.{}.{}-{}'.format(uncrypted_cpf[:3], uncrypted_cpf[3:6], uncrypted_cpf[6:9], uncrypted_cpf[9:])
    return render_template('cpf_key_form.html', cpf=uncrypted_cpf, form=form, title=title, paragraph=paragraph, registered=registered, parsed_cpf=parsed_cpf)

@pix_keys_controller.route('/cadaster-cpf-key', methods=['POST'])
def cadaster_cpf_key():
    form = PasswordConfirmForm()
    user_data = User.find_by_id(session.get('user_id'))
    
    if form.validate_on_submit():
        if check_password(form.password.data, user_data.password):
            user_data.registered_cpf_key = True
            db.session.commit()
            return render_template('success_register_pixkey.html')
        else:
            return jsonify({
                'password status': 'incorrect', 
                'response': 'failed', 
                'debug': {
                    'SENHA_DIGITADA': form.password.data,
                    'HASH_ARMAZENADO': user_data['password']
                }
            })
            
@pix_keys_controller.route('/phone-key-form')
def phone_key_form():
    form = PasswordConfirmForm()
    user_data = User.find_by_id(session.get('user_id'))
    phone = user_data.phone
    registered = False
    title = False
    paragraph = False
    
    if user_data.registered_phone_key:
        title = 'Você já tem uma chave pix registrada.'
        paragraph = 'Sua chave pix'
        registered = True
    
    uncrypted_phone = uncrypt_data(phone)
    send_notification(1, user_data.name, 12,'Confirme a Transação.')
    return render_template('phone_key_form.html', phone=uncrypted_phone, form=form, title=title, paragraph=paragraph, registered=registered)

@pix_keys_controller.route('/cadaster-phone-key', methods=['POST'])
def cadaster_phone_key():
    form = PasswordConfirmForm()
    user_data = User.find_by_id(session.get('user_id'))
    
    if form.validate_on_submit():
        if check_password(form.password.data, user_data.password):
            user_data.registered_phone_key = True
            db.session.commit()
            return render_template('success_register_pixkey.html')
        else:
            return jsonify({
                'password status': 'incorrect', 
                'response': 'failed', 
                'debug': {
                    'SENHA_DIGITADA': form.password.data,
                    'HASH_ARMAZENADO': user_data['password']
                }
            })
            
            
@pix_keys_controller.route('/email-key-form')
def email_key_form():
    form = PasswordConfirmForm()
    user_data = User.find_by_id(session.get('user_id'))
    email = user_data.email
    registered = False
    title = False
    paragraph = False
    
    if user_data.registered_email_key:
        title = 'Você já tem uma chave pix registrada.'
        paragraph = 'Sua chave pix'
        registered = True
    
    uncrypted_email = uncrypt_data(email)
    return render_template('email_key_form.html', email=uncrypted_email, form=form, title=title, paragraph=paragraph, registered=registered)

@pix_keys_controller.route('/cadaster-email-key', methods=['POST'])
def cadaster_email_key():
    form = PasswordConfirmForm()
    user_data = User.find_by_id(session.get('user_id'))
    
    if form.validate_on_submit():
        if check_password(form.password.data, user_data.password):
            user_data.registered_email_key = True
            db.session.commit()
            return render_template('success_register_pixkey.html')
        else:
            return jsonify({
                'password status': 'incorrect', 
                'response': 'failed', 
                'debug': {
                    'SENHA_DIGITADA': form.password.data,
                    'HASH_ARMAZENADO': user_data['password']
                }
            })
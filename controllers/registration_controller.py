from flask import Blueprint, render_template, redirect, url_for, session
from entry_forms.forms import RegistrationForm
from utils.utils import encrypt_data, validate_phone_numbers, hash_password
from models.db_models import User
from config import redis_methods_connection
import json

registrations_controller = Blueprint('registration_controller', __name__)

@registrations_controller.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    
    if form.validate_on_submit():
        
        encrypted_password = hash_password(form.password.data)
        encrypted_cpf = encrypt_data(form.cpf.data)
        encrypted_mail = encrypt_data(form.email.data)
        encrypted_phone = encrypt_data(form.phone.data)
        
        user = User.create_user(form.name.data, encrypted_password, encrypted_cpf, encrypted_mail, encrypted_phone)
        
        data = {
            'name': form.name.data,
            'balance': user.balance,
            'registered_cpf_key': user.registered_cpf_key,
            'registered_email_key': user.registered_email_key,
            'registered_phone_key': user.registered_phone_key
        }
        
        infos_user = json.dumps(data)
        
        session['user_id'] = user.id
        try:
            redis_methods_connection.insert(f'user:{user.id}', infos_user)
        except Exception as e:
            print(e)
        
        return redirect(url_for('home_controller.home'))
    
    return render_template('register.html', form=form)
from flask import Blueprint, render_template, session, jsonify, redirect, url_for
from models.db_models import User
from utils.utils import uncrypt_data, hash_password, check_password
from entry_forms.forms import RegisterCpfKeyForm
import bcrypt
from config import db
from config import redis_connection

pix_keys_controller = Blueprint('pix_keys_controller', __name__)

@pix_keys_controller.route('/cpf-key-form')
def cpf_key_form():
    form = RegisterCpfKeyForm()
    user_data = User.get_user_data(session.get('user_id'))
    cpf = user_data.cpf
    registered = False
    
    if user_data.registered_cpf_key:
        title = 'Você já tem uma chave pix registrada.'
        paragraph = 'Sua chave pix'
        registered = True
    
    uncrypted_cpf = uncrypt_data(cpf)
    parsed_cpf = '{}.{}.{}-{}'.format(uncrypted_cpf[:3], uncrypted_cpf[3:6], uncrypted_cpf[6:9], uncrypted_cpf[9:])
    return render_template('cpf_key_form.html', cpf=uncrypted_cpf, form=form, title=title, paragraph=paragraph, registered=registered, parsed_cpf=parsed_cpf)

@pix_keys_controller.route('/cadaster-cpf-key', methods=['POST'])
def cadaster_cpf_key():
    form = RegisterCpfKeyForm()
    user_data = User.get_user_data(session.get('user_id'))
    
    if form.validate_on_submit():
        if check_password(form.password.data, user_data.password):
            user_data.registered_cpf_key = True
            db.session.commit()
            return redirect(url_for('home_controller.home'))
        else:
            return jsonify({
                'password status': 'incorrect', 
                'response': 'failed', 
                'debug': {
                    'SENHA_DIGITADA': form.password.data,
                    'HASH_ARMAZENADO': user_data['password']
                }
            })

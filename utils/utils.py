import bcrypt
import phonenumbers
import hashlib
from config import redis_connection
import json


def update_user_balance(redis_connection, user_id, amount, is_payer=True):
    value = f"user:{user_id}"

    user = redis_connection.get(value).decode('utf-8')
    loaded_data = json.loads(user)

    # Subtrair o valor se for o pagador, adicionar se for o recebedor
    if is_payer:
        loaded_data['balance'] -= amount
    else:
        loaded_data['balance'] += amount

    updated_data = json.dumps(loaded_data)
    redis_connection.set(value, updated_data)

def hash_password(password):
    encoded_password = str(password).encode('utf-8')
    salt = bcrypt.gensalt()
    encrypted_data = bcrypt.hashpw(encoded_password, salt)
    
    return encrypted_data

def encrypt_data(data):
    encoded_data = str(data).encode('utf-8')
    encrypted_data = hashlib.sha256(encoded_data)
    
    return str(encrypted_data.hexdigest())
def verify_data(stored_data, data):
    data_encryptografed = encrypt_data(data)
    
    return stored_data == data_encryptografed

def validate_phone_numbers(phonenumber):
    try:
        phone = phonenumbers.parse(phonenumber)
        if not phonenumbers.is_valid_number(phone):
            return False
    except phonenumbers.NumberParseException as error:
        return False
    
    return True
    
    
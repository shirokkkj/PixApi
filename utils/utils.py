import bcrypt
import phonenumbers
import hashlib
from config import redis_connection
import json
from cryptography.fernet import Fernet
from dotenv import load_dotenv
import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64

load_dotenv()

key_64 = f'{os.getenv('KEY')}'# 32 bytes for AES-256
key = bytes.fromhex(key_64)
iv = f'{os.getenv('IV')}'.encode('utf-8')


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


def check_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))



def encrypt_data(data):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    parsed_data = pad(data.encode('utf-8'), AES.block_size)
    encrypted_data = cipher.encrypt(parsed_data)
    return base64.b64encode(encrypted_data).decode('utf-8')

def uncrypt_data(data):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    encrypted = base64.b64decode(data)
    padded_message = cipher.decrypt(encrypted)
    return unpad(padded_message, AES.block_size).decode('utf-8')

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
    
    
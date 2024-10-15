from config import socketio
from flask import request, session
from flask_socketio import join_room, emit
from models.db_models import Transactions, User


user_rooms = {}

@socketio.on('connect')
def connected():
    user_id = session.get('user_id')
    print(user_id)
    if user_id:
        user_rooms[user_id] = request.sid
        join_room(user_rooms[user_id])
        
def send_notification(user_id, sender, id_transaction, payer_id, cpf_payee, account_to_send, amount):
    room = user_rooms.get(user_id)
    if room:
        socketio.emit('notification', {'sender': sender, 'id': id_transaction, 'payer_id': payer_id, 'cpf_payee': cpf_payee, 'account_to_send': account_to_send, 'amount': amount}, room=room)
        print(f'Notification sent to room: {room}')
        
@socketio.on('confirmed_transaction')
def confirm_transaction_client(data):
    print(data)
    id_transaction = data['id']
    Transactions.confirm_payee_transaction(id_transaction)
    print('Confirmed Payee.')

    User.make_split_transaction_by_cpf(data['payer_id'], data['payee_cpf'],  data['account_to_send'],  quantity=data['quantity'])



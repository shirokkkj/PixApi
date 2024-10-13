from config import db
import datetime
from utils.utils import uncrypt_data

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False, unique=True)
    cpf = db.Column(db.String(255), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    phone = db.Column(db.String(255), nullable=False, unique=True)
    balance = db.Column(db.Float, nullable=True, default=0.0)
    secret_key = db.Column(db.String(255), nullable=True)
    registered_cpf_key = db.Column(db.Boolean, default=False)
    registered_email_key = db.Column(db.Boolean, default=False)
    registered_phone_key = db.Column(db.Boolean, default=False)

    def create_user(name, password, cpf, email, phone):
        user = User(name=name, password=password, cpf=cpf, email=email, phone=phone)
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def find_by_id(id):
        return User.query.filter_by(id=id).first()

    @staticmethod
    def find_by_secret_key(secret_key):
        return User.query.filter_by(secret_key=secret_key).first()

    @staticmethod
    def find_by_cpf(cpf):
        users = User.query.all()
        for user in users:
            if uncrypt_data(user.cpf) == cpf: 
                return user

    @staticmethod
    def find_by_email(email):
        users = User.query.all()
        for user in users:
            if uncrypt_data(user.email) == email: 
                return user

    @staticmethod
    def find_by_phone(phone):
        users = User.query.all()
        for user in users:
            if uncrypt_data(user.phone) == phone: 
                return user

    @staticmethod
    def process_transaction(payer, payee, quantity):
        if payer.balance < quantity:
            return {'status': 'fail', 'reason': 'Not enough money.'}

        payer.balance -= quantity
        payee.balance += quantity
        db.session.commit()

        return {'status': 'success', 'payer': payer.name, 'payee': payee.name, 'quantity': quantity}
    
    @staticmethod
    def make_transaction_by_secretkey(payer_id, secret_key, quantity):
        payer = User.find_by_id(payer_id)
        if not payer:
            return {'status': 'fail', 'reason': 'Pagador não encontrado.'}

        payee = User.find_by_secret_key(secret_key)
        if not payee:
            return {'status': 'fail', 'reason': 'Recebedor não encontrado.'}
        

        if payee == payer:
            return {'status': 'fail', 'reason': 'O pagador não pode ser o mesmo que o recebedor.'}

        return User.process_transaction(payer, payee, quantity)
    @staticmethod
    def make_transaction_by_cpf(payer_id, cpf, quantity):
        payer = User.find_by_id(payer_id)
        if not payer:
            return {'status': 'fail', 'reason': 'Pagador não encontrado.'}

        payee = User.find_by_cpf(cpf)
        if not payee:
            return {'status': 'fail', 'reason': 'Recebedor não encontrado.'}

        if not payee.registered_cpf_key:
            return {'status': 'fail', 'reason': 'O recebedor não possui uma chave pix de CPF registrada.'}

        if payee == payer:
            return {'status': 'fail', 'reason': 'O pagador não pode ser o mesmo que o recebedor.'}

        return User.process_transaction(payer, payee, quantity)
    @staticmethod
    def make_transaction_by_email(payer_id, email, quantity):
        payer = User.find_by_id(payer_id)
        if not payer:
            return {'status': 'fail', 'reason': 'Pagador não encontrado.'}

        payee = User.find_by_email(email)
        if not payee:
            return {'status': 'fail', 'reason': 'Recebedor não encontrado.'}
        
        if not payee.registered_email_key:
            return {'status': 'fail', 'reason': 'O recebedor não possui uma chave pix de e-mail registrada.'}

        if payee == payer:
            return {'status': 'fail', 'reason': 'O pagador não pode ser o mesmo que o recebedor.'}

        return User.process_transaction(payer, payee, quantity)
    @staticmethod
    def make_transaction_by_phone(payer_id, phone, quantity):
        payer = User.find_by_id(payer_id)
        if not payer:
            return {'status': 'fail', 'reason': 'Pagador não encontrado.'}

        payee = User.find_by_phone(phone)
        if not payee:
            return {'status': 'fail', 'reason': 'Recebedor não encontrado.'}
        
        if not payee.registered_phone_key:
            return {'status': 'fail', 'reason': 'O recebedor não possui uma chave pix de celular registrada.'}

        if payee == payer:
            return {'status': 'fail', 'reason': 'O pagador não pode ser o mesmo que o recebedor.'}

        return User.process_transaction(payer, payee, quantity)

    
    
        
    
class Transactions(db.Model):
    __tablename__ = 'transations'
    
    id = db.Column(db.Integer, primary_key = True)
    id_payer = db.Column(db.Integer, nullable = False)
    name_payer = db.Column(db.String(255), nullable = False)
    id_receiver = db.Column(db.Integer, nullable = False)
    name_receiver = db.Column(db.String(255), nullable = False)
    id_transaction = db.Column(db.String(255), nullable = False)
    amount = db.Column(db.Float, nullable = False)
    date = db.Column(db.Date, default=datetime.date.today())
    
    def make_transation(id_payer, name_payer, id_receiver, name_receiver, id_transaction, amount):
        try:
            new_transation = Transactions(id_payer=id_payer, name_payer=name_payer, id_receiver=id_receiver, name_receiver=name_receiver, id_transaction=id_transaction, amount=amount)
            db.session.add(new_transation)
            db.session.commit()
            return {'status': 'success'}
        except Exception as e:
            db.session.rollback()
            return {'status': 'fail', 'reason': 'Ocorreu um erro ao processar a transação.'}  
        
    def get_payment_transactions(user_id):
        transactions = Transactions.query.filter_by(id_payer=user_id).all()
        return transactions
    
    def get_recebment_transactions(user_id):
        transactions = Transactions.query.filter_by(id_receiver=user_id).all()
        return transactions
    
    def get_transactions_by_date(date):
        parsed_date = datetime.datetime.strftime(date, '%Y/%m/%d')
        transactions = Transactions.query.filter(Transactions.date == parsed_date).all()
        return transactions
    
    
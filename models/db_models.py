from config import db
import datetime
from utils.utils import encrypt_data
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
        return User.query.filter_by(cpf=cpf).first()

    @staticmethod
    def find_by_email(email):
        return User.query.filter_by(email=email).first()

    @staticmethod
    def find_by_phone(phone):
        return User.query.filter_by(phone=phone).first()

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

        payee = User.find_by_cpf(encrypt_data(cpf))
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

        payee = User.find_by_email(encrypt_data(email))
        if not payee:
            return {'status': 'fail', 'reason': 'Recebedor não encontrado.'}
        
        if not payee.registered_email_key:
            return {'status': 'fail', 'reason': 'O recebedor não possui uma chave pix de e-mail registrada.'}

        if payee == payer:
            return {'status': 'fail', 'reason': 'O pagador não pode ser o mesmo que o recebedor.'}

        return User.process_transaction(payer, payee, quantity)
    
    @staticmethod
    def make_split_transaction_by_cpf(payer_id, payee_cpf, account_to_send, quantity):
        payer = User.find_by_id(payer_id)
        if not payer:
            return {'status': 'fail', 'reason': 'Pagador não encontrado.'}

        payee = User.find_by_cpf(encrypt_data(payee_cpf))
        if not payee:
            return {'status': 'fail', 'reason': 'Recebedor não encontrado.'}
        
        if payee == payer:
            return {'status': 'fail', 'reason': 'O pagador não pode ser o mesmo que o recebedor.'}
        
        if payer.balance < quantity:
            return {'status': 'fail', 'reason': 'Not enough money.'}
        
        receiver_account = User.find_by_cpf(encrypt_data(account_to_send))
        
        payer.balance -= quantity / 2
        payee.balance -= quantity / 2
        receiver_account.balance += quantity
        db.session.commit()
        
        return {'status': 'success'}
        
    @staticmethod
    def make_transaction_by_phone(payer_id, phone, quantity):
        payer = User.find_by_id(payer_id)
        if not payer:
            return {'status': 'fail', 'reason': 'Pagador não encontrado.'}

        payee = User.find_by_phone(encrypt_data(phone))
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
    status = db.Column(db.String(15), default='Pending')
    type = db.Column(db.String(15), default='Unique', nullable=True)
    payee_has_confirmed = db.Column(db.Boolean, default=False, nullable=True)
    
    @staticmethod
    def make_transation(id_payer, name_payer, id_receiver, name_receiver, id_transaction, amount, type='Unique'):
        try:
            new_transation = Transactions(id_payer=id_payer, name_payer=name_payer, id_receiver=id_receiver, name_receiver=name_receiver, id_transaction=id_transaction, amount=amount, type=type)
            db.session.add(new_transation)
            db.session.commit()
            return new_transation
        except Exception as e:
            db.session.rollback()
            return {'status': 'fail', 'reason': e}  
    @staticmethod
    def get_payment_transactions(user_id):
        transactions = Transactions.query.filter_by(id_payer=user_id).all()
        return transactions
    @staticmethod
    def get_recebment_transactions(user_id):
        transactions = Transactions.query.filter_by(id_receiver=user_id).all()
        return transactions
    @staticmethod
    def get_transactions_by_date(date):
        parsed_date = datetime.datetime.strftime(date, '%Y/%m/%d')
        transactions = Transactions.query.filter(Transactions.date == parsed_date).all()
        return transactions
    @staticmethod
    def get_transaction_by_id(id):
        return Transactions.query.filter_by(id=id).first()
    
    @staticmethod
    def confirm_payee_transaction(id_transaction):
        try:
            transaction = Transactions.get_transaction_by_id(id_transaction)
            transaction.payee_has_confirmed = True
            db.session.commit()
            db.session.expire_all()
            print(transaction.payee_has_confirmed)
        except Exception as e:
            print(e)
        
    @staticmethod
    def has_payee_confirmated(id_transaction):
        transaction = Transactions.get_transaction_by_id(id_transaction)
        
        if transaction.payee_has_confirmed:
            return {'status': 'success', 'message': 'Payee has been confirmated the transaction.'}
        
        else:
            return {"status": 'fail', 'message': 'Payee do not confirmated the transaction.'}
        
    @staticmethod
    def confirm_transaction(id_transaction, payer, cpf, amount):
        if not Transactions.confirm_payee_transaction(id_transaction)['status'] == 'success':
          return
        if not Transactions.has_payee_confirmated(id_transaction)['status'] == 'success':
            return
        
        User.make_transaction_by_cpf(payer.id, cpf, float(amount) / 2)  
        
        
    # Ok, i go to make the Front-End (i dont will show this part in video) and comeback. Wait me!
        
        
        
        
    
    
    
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('postgresql://postgres:postgres@localhost:5432/moses', echo=True)
Base = declarative_base()

class Customer(Base):
    __tablename__ = 'customer1'
    id = Column(Integer, primary_key=True)
    nama = Column(String)
    alamat = Column(String)

class Account(Base):
    __tablename__ = 'account'
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer)
    nomor = Column(String)
    balance = Column(Integer)

class trans_log(Base):
    __tablename__ = 'trans_log2'
    id = Column(Integer, primary_key=True)
    account_id = Column(Integer)
    amount = Column(Integer)
    balance = Column(Integer)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

a = session.query(Customer).delete()
b = session.query(Account).delete()
c = session.query(trans_log).delete()
session.commit()

bapak = Customer(nama='bapak', alamat='jln hongkong')
ibu = Customer(nama='ibu', alamat='jln singapura')
masyo = Customer(nama='masyo', alamat='jln setip')
moses = Customer(nama='moses', alamat='jln setipi')
session.bulk_save_objects([bapak, ibu, masyo, moses], return_defaults=True)
session.commit()

bapak1 = Account(customer_id=bapak.id, nomor='789', balance=1000)
ibu1 = Account(customer_id=ibu.id, nomor='778', balance=1000)
masyo1 = Account(customer_id=masyo.id, nomor='888', balance=1000)
moses1 = Account(customer_id=moses.id, nomor='889', balance=1000)
session.bulk_save_objects([bapak1, ibu1, masyo1, moses1], return_defaults=True)
session.commit()

def log_entries(func):
    def wrapper(*args):
        result = func(*args)
        print(args[0].id)
        y = trans_log(account_id=args[0].id, amount=args[1], balance=result)
        session.add(y)
        return result
    return wrapper

@log_entries
def set_balance(account, nilai_amount):
    account.balance += nilai_amount
    return account.balance

def transfer(account1, account2, amount):
    set_balance(account1, -amount)
    set_balance(account2, amount)
    
transfer(bapak1, moses1, 100)
transfer(bapak1, ibu1, 75)
transfer(bapak1, masyo1, 70)
session.commit()
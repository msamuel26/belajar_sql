from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('postgresql://postgres:postgres@localhost:5432/moses', echo=True)
Base = declarative_base()

class Users(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    balance = Column(Integer)

class Logs(Base):
    __tablename__ = 'trans_log'
    id = Column(Integer, primary_key=True)
    nama = Column(String)
    amount = Column(Integer)
    balance = Column(Integer)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

def my_log(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        log = Logs(nama=args[0].name, amount=args[1], balance=result)
        session.add(log)
        return result
    return wrapper

@my_log
def set_balance(user, nilai_amount):
    user.balance += nilai_amount
    return user.balance

a = session.query(Users).delete()
b = session.query(Logs).delete()
session.commit()

setipi = Users(name='Setipi', balance=70)
mcpout = Users(name='McPout', balance=70)
session.add(setipi)
session.add(mcpout)
session.commit()

value = 30
while setipi.balance > 0:
    # setipi.balance -= value
    set_balance(setipi, -value)
    # mcpout.balance += value
    set_balance(mcpout, value) 
    if setipi.balance < 0:
        session.rollback()
        break
    else:
        session.commit()
    print(f"Setipi's balance: {setipi.balance}")
    print(f"McPout's balance: {mcpout.balance}")

session.close()


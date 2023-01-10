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

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

a = session.query(Users).delete()
session.commit()

setipi = Users(name='Setipi', balance=70)
mcpout = Users(name='McPout', balance=70)
session.add(setipi)
session.add(mcpout)
session.commit()

value = 30
while setipi.balance > 0:
    setipi.balance -= value
    mcpout.balance += value
    if setipi.balance < 0:
        session.rollback()
        break
    else:
        session.commit()
    print(f"Setipi's balance: {setipi.balance}")
    print(f"McPout's balance: {mcpout.balance}")

    # Setipi's balance: 40
    # McPout's balance: 100
    # Setipi's balance: 10
    # McPout's balance: 130

session.close()
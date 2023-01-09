from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Set up the database
engine = create_engine('postgresql://postgres:postgres@localhost:5432/moses', echo=True)
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    balance = Column(Integer)

Base.metadata.create_all(engine)

# Create a session to add users to the database
Session = sessionmaker(bind=engine)
session = Session()

print("proses delete data\n")
a = session.query(User).delete()
session.commit()

# 2023-01-09 21:46:05,332 INFO sqlalchemy.engine.Engine BEGIN (implicit)
# 2023-01-09 21:46:05,340 INFO sqlalchemy.engine.Engine DELETE FROM users
# 2023-01-09 21:46:05,340 INFO sqlalchemy.engine.Engine [generated in 0.00066s] {}
# 2023-01-09 21:46:05,340 INFO sqlalchemy.engine.Engine COMMIT


# Add Bob and Alice to the database
print("memasukkan Bob dan Alice ke dalam database\n")
bob = User(name='Bob', balance=50)
alice = User(name='Alice', balance=50)
session.add(bob)
session.add(alice)
session.commit()

# 2023-01-09 21:46:05,348 INFO sqlalchemy.engine.Engine BEGIN (implicit)
# 2023-01-09 21:46:05,348 INFO sqlalchemy.engine.Engine INSERT INTO users (name, balance) VALUES 
# (%(name)s, %(balance)s) RETURNING users.id
# 2023-01-09 21:46:05,348 INFO sqlalchemy.engine.Engine [generated in 0.00102s] ({'name': 'Bob', 
# 'balance': 50}, {'name': 'Alice', 'balance': 50})
# 2023-01-09 21:46:05,356 INFO sqlalchemy.engine.Engine COMMIT


# Create multiple transfer transactions between Bob and Alice
value = 40
while bob.balance > 0:
    bob.balance -= value
    alice.balance += value
    if bob.balance < 0:
        session.rollback()
        break
    else:
        session.commit()
    print(f'Bob\'s balance: {bob.balance}')
    print(f'Alice\'s balance: {alice.balance}')

# 2023-01-09 21:49:06,166 INFO sqlalchemy.engine.Engine BEGIN (implicit)
# 2023-01-09 21:49:06,166 INFO sqlalchemy.engine.Engine SELECT users.id AS users_id, users.name AS users_name, users.balance AS users_balance
# FROM users
# WHERE users.id = %(pk_1)s
# 2023-01-09 21:49:06,166 INFO sqlalchemy.engine.Engine [generated in 0.00107s] {'pk_1': 31}     
# 2023-01-09 21:49:06,174 INFO sqlalchemy.engine.Engine UPDATE users SET balance=%(balance)s WHERE users.id = %(users_id)s
# 2023-01-09 21:49:06,174 INFO sqlalchemy.engine.Engine [generated in 0.00090s] {'balance': 10, 'users_id': 31}
# 2023-01-09 21:49:06,174 INFO sqlalchemy.engine.Engine SELECT users.id AS users_id, users.name AS users_name, users.balance AS users_balance
# FROM users
# WHERE users.id = %(pk_1)s
# 2023-01-09 21:49:06,182 INFO sqlalchemy.engine.Engine [cached since 0.0108s ago] {'pk_1': 32}
# 2023-01-09 21:49:06,182 INFO sqlalchemy.engine.Engine UPDATE users SET balance=%(balance)s WHERE users.id = %(users_id)s
# 2023-01-09 21:49:06,182 INFO sqlalchemy.engine.Engine [cached since 0.007905s ago] {'balance': 
# 90, 'users_id': 32}
# 2023-01-09 21:49:06,182 INFO sqlalchemy.engine.Engine COMMIT
# 2023-01-09 21:49:06,182 INFO sqlalchemy.engine.Engine BEGIN (implicit)
# 2023-01-09 21:49:06,190 INFO sqlalchemy.engine.Engine SELECT users.id AS users_id, users.name AS users_name, users.balance AS users_balance
# FROM users
# WHERE users.id = %(pk_1)s
# 2023-01-09 21:49:06,190 INFO sqlalchemy.engine.Engine [cached since 0.01983s ago] {'pk_1': 31} 
# Bob's balance: 10
# 2023-01-09 21:49:06,190 INFO sqlalchemy.engine.Engine SELECT users.id AS users_id, users.name AS users_name, users.balance AS users_balance
# FROM users
# WHERE users.id = %(pk_1)s
# 2023-01-09 21:49:06,190 INFO sqlalchemy.engine.Engine [cached since 0.02381s ago] {'pk_1': 32} 
# Alice's balance: 90
# 2023-01-09 21:49:06,190 INFO sqlalchemy.engine.Engine ROLLBACK

session.close()
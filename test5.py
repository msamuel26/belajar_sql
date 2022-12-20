from sqlalchemy import create_engine, Integer, Sequence, Column, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Customer(Base):
    __tablename__ = 'customer'
    id = Column(Integer, Sequence('customer_id_seq'), primary_key=True)
    name = Column(String)
    address = Column(String)

class Order(Base):
    __tablename__ = 'order'

    id = Column(Integer, Sequence('order_id_seq'), primary_key=True)
    product = Column(String)
    customer_id = Column(Integer, ForeignKey('customer.id'))

engine = create_engine("sqlite:///relasi.db", echo=True)

Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()

# a = session.query(Order).filter(Order.id > 0).delete()
# b = session.query(Customer).filter(Customer.id > 0).delete()
# session.commit()

# Membuat objek customer baru
print("insert data customer")
new_customer = Customer(name='John', address='New York')

# Menambahkan objek customer baru ke dalam session
print("menambahkan data customer baru ke session")
session.add(new_customer)

# Commit perubahan ke database
print("commit ke database")
session.commit()

# 2022-12-20 11:24:09,519 INFO sqlalchemy.engine.Engine BEGIN (implicit)
# 2022-12-20 11:24:09,519 INFO sqlalchemy.engine.Engine INSERT INTO customer (name, address) VALUES (?, ?)
# 2022-12-20 11:24:09,519 INFO sqlalchemy.engine.Engine [generated in 0.00105s] ('John', 'New York')
# 2022-12-20 11:24:09,530 INFO sqlalchemy.engine.Engine COMMIT

# Membuat objek order baru
print("insert data order")
new_order = Order(product='Apple', customer_id=new_customer.id)

# 2022-12-20 11:24:09,551 INFO sqlalchemy.engine.Engine BEGIN (implicit)
# 2022-12-20 11:24:09,559 INFO sqlalchemy.engine.Engine SELECT customer.id AS customer_id, customer.name AS customer_name, customer.address AS customer_address
# FROM customer
# WHERE customer.id = ?
# 2022-12-20 11:24:09,559 INFO sqlalchemy.engine.Engine [generated in 0.00129s] (7,)

# Menambahkan objek order baru ke dalam session
print("menambahkan data order baru ke session")
session.add(new_order)

# Commit perubahan ke database
print("commit ke database (1)")
session.commit()

# 2022-12-20 11:24:09,567 INFO sqlalchemy.engine.Engine INSERT INTO "order" (product, customer_id) VALUES (?, ?)
# 2022-12-20 11:24:09,567 INFO sqlalchemy.engine.Engine [generated in 0.00134s] ('Apple', 7)     
# 2022-12-20 11:24:09,567 INFO sqlalchemy.engine.Engine COMMIT

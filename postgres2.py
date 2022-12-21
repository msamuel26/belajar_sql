from sqlalchemy import create_engine, Integer, Sequence, Column, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Customer(Base):
    # nama tabel agar menggunakan huruf kecil
    __tablename__ = 'customer'
    id = Column("id", Integer, Sequence("customer_id_seq"), primary_key=True)
    first_name = Column("first_name", String)
    last_name = Column("last_name", String)
    age = Column("age", Integer)
    country = Column("country", String)

class Order(Base):
    # nama tabel agar menggunakan huruf kecil
    __tablename__ = 'order'
    id = Column("id", Integer, Sequence("order_id_seq"), primary_key=True)
    item = Column("item", String)
    amount = Column("amount", Integer)
    customer_id = Column("customer_id", Integer, ForeignKey('customer.id'))

conn_string = 'postgresql://postgres:postgres@localhost:5432/moses'

engine = create_engine(conn_string, echo=True)

Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()

a = session.query(Order).filter(Order.id > 0).delete()
b = session.query(Customer).filter(Customer.id > 0).delete()
session.commit()

print("insert multiple data ke dalam customer")
new_customer = Customer(first_name='John', last_name='Doe', age=31, country='USA')
new_customer1 = Customer(first_name='Robert', last_name='Luna', age=22, country='USA')
new_customer2 = Customer(first_name='David', last_name='Robinson', age=22, country='UK')
new_customer3 = Customer(first_name='John', last_name='Reinhardt', age=25, country='UK')
new_customer4 = Customer(first_name='Betty', last_name='Doe', age=28, country='UAE')

session.bulk_save_objects([new_customer, new_customer1, new_customer2,
             new_customer3, new_customer4], return_defaults=True)
session.commit()

# 2022-12-20 12:01:09,573 INFO sqlalchemy.engine.Engine BEGIN (implicit)
# 2022-12-20 12:01:09,573 INFO sqlalchemy.engine.Engine INSERT INTO customer (first_name, last_name, age, country) VALUES (?, ?, ?, ?)
# 2022-12-20 12:01:09,573 INFO sqlalchemy.engine.Engine [generated in 0.00127s] ('John', 'Doe', 31, 'USA')
# 2022-12-20 12:01:09,581 INFO sqlalchemy.engine.Engine INSERT INTO customer (first_name, last_name, age, country) VALUES (?, ?, ?, ?)
# 2022-12-20 12:01:09,581 INFO sqlalchemy.engine.Engine [cached since 0.009067s ago] ('Robert', 'Luna', 22, 'USA')
# 2022-12-20 12:01:09,581 INFO sqlalchemy.engine.Engine INSERT INTO customer (first_name, last_name, age, country) VALUES (?, ?, ?, ?)
# 2022-12-20 12:01:09,581 INFO sqlalchemy.engine.Engine [cached since 0.01108s ago] ('David', 'Robinson', 22, 'UK')
# 2022-12-20 12:01:09,581 INFO sqlalchemy.engine.Engine INSERT INTO customer (first_name, last_name, age, country) VALUES (?, ?, ?, ?)
# 2022-12-20 12:01:09,581 INFO sqlalchemy.engine.Engine [cached since 0.01237s ago] ('John', 'Reinhardt', 25, 'UK')
# 2022-12-20 12:01:09,581 INFO sqlalchemy.engine.Engine INSERT INTO customer (first_name, last_name, age, country) VALUES (?, ?, ?, ?)
# 2022-12-20 12:01:09,581 INFO sqlalchemy.engine.Engine [cached since 0.01376s ago] ('Betty', 'Doe', 28, 'UAE')
# 2022-12-20 12:01:09,592 INFO sqlalchemy.engine.Engine COMMIT

print("insert multiple data ke dalam order")
new_order1 = Order(item='Keyboard', amount=400, customer_id=new_customer3.id)
new_order2 = Order(item='Mouse', amount=300, customer_id=new_customer3.id)
new_order3= Order(item='Monitor', amount=12000, customer_id=new_customer2.id)
new_order4 = Order(item='Keyboard', amount=400, customer_id=new_customer.id)
new_order5 = Order(item='Mousepad', amount=250, customer_id=new_customer1.id)

session.bulk_save_objects([new_order1, new_order2, new_order3, new_order4])
session.commit()

# 2022-12-20 12:01:09,602 INFO sqlalchemy.engine.Engine BEGIN (implicit)
# 2022-12-20 12:01:09,612 INFO sqlalchemy.engine.Engine SELECT customer.id AS customer_id, customer.first_name AS customer_first_name, customer.last_name AS customer_last_name, customer.age AS customer_age, customer.country AS customer_country
# FROM customer
# WHERE customer.id = ?
# 2022-12-20 12:01:09,612 INFO sqlalchemy.engine.Engine [generated in 0.00124s] (9,)
# 2022-12-20 12:01:09,612 INFO sqlalchemy.engine.Engine SELECT customer.id AS customer_id, customer.first_name AS customer_first_name, customer.last_name AS customer_last_name, customer.age AS customer_age, customer.country AS customer_country
# FROM customer
# WHERE customer.id = ?
# 2022-12-20 12:01:09,612 INFO sqlalchemy.engine.Engine [cached since 0.004633s ago] (8,)        
# 2022-12-20 12:01:09,612 INFO sqlalchemy.engine.Engine SELECT customer.id AS customer_id, customer.first_name AS customer_first_name, customer.last_name AS customer_last_name, customer.age AS customer_age, customer.country AS customer_country
# FROM customer
# WHERE customer.id = ?
# 2022-12-20 12:01:09,622 INFO sqlalchemy.engine.Engine [cached since 0.008788s ago] (6,)
# 2022-12-20 12:01:09,622 INFO sqlalchemy.engine.Engine SELECT customer.id AS customer_id, customer.first_name AS customer_first_name, customer.last_name AS customer_last_name, customer.age AS customer_age, customer.country AS customer_country
# FROM customer
# WHERE customer.id = ?
# 2022-12-20 12:01:09,622 INFO sqlalchemy.engine.Engine [cached since 0.0113s ago] (7,)
# 2022-12-20 12:01:09,622 INFO sqlalchemy.engine.Engine INSERT INTO "order" (item, amount, customer_id) VALUES (?, ?, ?)
# 2022-12-20 12:01:09,622 INFO sqlalchemy.engine.Engine [generated in 0.00112s] ('Keyboard', 400, 9)
# 2022-12-20 12:01:09,632 INFO sqlalchemy.engine.Engine INSERT INTO "order" (item, amount, customer_id) VALUES (?, ?, ?)
# 2022-12-20 12:01:09,632 INFO sqlalchemy.engine.Engine [cached since 0.00519s ago] ('Mouse', 300, 9)
# 2022-12-20 12:01:09,632 INFO sqlalchemy.engine.Engine INSERT INTO "order" (item, amount, customer_id) VALUES (?, ?, ?)
# 2022-12-20 12:01:09,632 INFO sqlalchemy.engine.Engine [cached since 0.006669s ago] ('Monitor', 
# 12000, 8)
# 2022-12-20 12:01:09,632 INFO sqlalchemy.engine.Engine INSERT INTO "order" (item, amount, customer_id) VALUES (?, ?, ?)
# 2022-12-20 12:01:09,632 INFO sqlalchemy.engine.Engine [cached since 0.008336s ago] ('Keyboard', 400, 6)
# 2022-12-20 12:01:09,632 INFO sqlalchemy.engine.Engine INSERT INTO "order" (item, amount, customer_id) VALUES (?, ?, ?)
# 2022-12-20 12:01:09,632 INFO sqlalchemy.engine.Engine [cached since 0.01024s ago] ('Mousepad', 
# 250, 7)
# 2022-12-20 12:01:09,632 INFO sqlalchemy.engine.Engine COMMIT


engine.execute("insert into customer (id, first_name, last_name, age, country) values (6, 'Setip', 'Cengiri', 7, 'IDN')")

print("menutup sesi transaction/koneksi ke database")
# bertujuan untuk menutup sesi transaction/koneksi ke database
session.close()


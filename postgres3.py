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

print("insert multiple data ke dalam customer (0-4)\n")
new_customer = Customer(first_name='John', last_name='Doe', age=31, country='USA')
new_customer1 = Customer(first_name='Robert', last_name='Luna', age=22, country='USA')
new_customer2 = Customer(first_name='David', last_name='Robinson', age=22, country='UK')
new_customer3 = Customer(first_name='John', last_name='Reinhardt', age=25, country='UK')
new_customer4 = Customer(first_name='Betty', last_name='Doe', age=28, country='UAE')

# return_defaults=True berarti SQL yang dihasilkan SQLAlchemy akan meng-return ID
print("masukkan banyak data (0-4) ke dalam tabel database customer dalam 1 line code, dengan return_defaults=True\n")
session.bulk_save_objects([new_customer, new_customer1, new_customer2,
             new_customer3, new_customer4], return_defaults=True)
session.commit()

# 2022-12-21 14:12:37,702 INFO sqlalchemy.engine.Engine BEGIN (implicit)
# 2022-12-21 14:12:37,705 INFO sqlalchemy.engine.Engine INSERT INTO customer (id, first_name, last_name, age, country) VALUES (nextval('customer_id_seq'), %(first_name)s, %(last_name)s, %(age)s, %(country)s) RETURNING customer.id
# 2022-12-21 14:12:37,705 INFO sqlalchemy.engine.Engine [generated in 0.00063s] ({'first_name': 'John', 'last_name': 'Doe', 'age': 31, 'country': 'USA'}, {'first_name': 'Robert', 'last_name': 
# 'Luna', 'age': 22, 'country': 'USA'}, {'first_name': 'David', 'last_name': 'Robinson', 'age': 22, 'country': 'UK'}, {'first_name': 'John', 'last_name': 'Reinhardt', 'age': 25, 'country': 'UK'}, {'first_name': 'Betty', 'last_name': 'Doe', 'age': 28, 'country': 'UAE'})
# 2022-12-21 14:12:37,709 INFO sqlalchemy.engine.Engine COMMIT

print("insert multiple data ke dalam customer (5-9)\n")
new_customer5 = Customer(first_name='Mike', last_name='Johnson', age=22, country='USA')
new_customer6 = Customer(first_name='David', last_name='Christian', age=28, country='UK')
new_customer7 = Customer(first_name='Robert', last_name='Bob', age=25, country='UK')
new_customer8 = Customer(first_name='Alice', last_name='Johnson', age=23, country='USA')
new_customer9 = Customer(first_name='Valentino', last_name='Robert', age=20, country='ITA')

# return_defaults=False berarti SQL yang dihasilkan SQLAlchemy tidak akan meng-return ID
print("masukkan banyak data ke dalam tabel database customer dalam 1 line code, dengan return_defaults=False\n")
session.bulk_save_objects([new_customer5, new_customer6, new_customer7, new_customer8, new_customer9], return_defaults=False)
session.commit()

# 2022-12-21 14:12:37,712 INFO sqlalchemy.engine.Engine BEGIN (implicit)
# 2022-12-21 14:12:37,713 INFO sqlalchemy.engine.Engine INSERT INTO customer (id, first_name, last_name, age, country) VALUES (nextval('customer_id_seq'), %(first_name)s, %(last_name)s, %(age)s, %(country)s)
# 2022-12-21 14:12:37,713 INFO sqlalchemy.engine.Engine [generated in 0.00079s] ({'first_name': 'Mike', 'last_name': 'Johnson', 'age': 22, 'country': 'USA'}, {'first_name': 'David', 'last_name': 'Christian', 'age': 28, 'country': 'UK'}, {'first_name': 'Robert', 'last_name': 'Bob', 'age': 25, 'country': 'UK'}, {'first_name': 'Alice', 'last_name': 'Johnson', 'age': 23, 'country': 'USA'}, {'first_name': 'Valentino', 'last_name': 'Robert', 'age': 20, 'country': 'ITA'})        
# 2022-12-21 14:12:37,714 INFO sqlalchemy.engine.Engine COMMIT

print("insert multiple data ke dalam order (1-5)\n")
new_order1 = Order(item='Keyboard', amount=400, customer_id=new_customer3.id)
new_order2 = Order(item='Mouse', amount=300, customer_id=new_customer3.id)
new_order3 = Order(item='Monitor', amount=12000, customer_id=new_customer2.id)
new_order4 = Order(item='Keyboard', amount=400, customer_id=new_customer.id)
new_order5 = Order(item='Mousepad', amount=250, customer_id=new_customer1.id)

print("masukkan banyak data (1-5) ke dalam tabel database order dalam 1 line code, lalu commit\n")
session.bulk_save_objects([new_order1, new_order2, new_order3, new_order4, new_order5])
session.commit()

# 2022-12-21 14:12:37,715 INFO sqlalchemy.engine.Engine BEGIN (implicit)
# 2022-12-21 14:12:37,716 INFO sqlalchemy.engine.Engine INSERT INTO "order" (id, item, amount, customer_id) VALUES (nextval('order_id_seq'), %(item)s, %(amount)s, %(customer_id)s)
# 2022-12-21 14:12:37,717 INFO sqlalchemy.engine.Engine [generated in 0.00056s] ({'item': 'Keyboard', 'amount': 400, 'customer_id': 54}, {'item': 'Mouse', 'amount': 300, 'customer_id': 54}, {'item': 'Monitor', 'amount': 12000, 'customer_id': 53}, {'item': 'Keyboard', 'amount': 400, 'customer_id': 51}, {'item': 'Mousepad', 'amount': 250, 'customer_id': 52})
# 2022-12-21 14:12:37,722 INFO sqlalchemy.engine.Engine COMMIT

print("insert multiple data ke dalam order (6-10)\n")
new_order6 = Order(item='Keypad', amount=2000, customer_id=new_customer6.id)
new_order7 = Order(item='Laptop', amount=15000, customer_id=new_customer8.id)
new_order8 = Order(item='GPU', amount=10000, customer_id=new_customer7.id)
new_order9 = Order(item='Motherboard', amount=9000, customer_id=new_customer5.id)
new_order10 = Order(item='CPU Cooler', amount=7500, customer_id=new_customer7.id)

print("masukkan banyak data (6-10) ke dalam tabel database order dalam 1 line code, lalu commit\n")
session.bulk_save_objects([new_order6, new_order7, new_order8, new_order9, new_order10])
session.commit()

# 2022-12-21 14:12:37,723 INFO sqlalchemy.engine.Engine BEGIN (implicit)
# 2022-12-21 14:12:37,724 INFO sqlalchemy.engine.Engine INSERT INTO "order" (id, item, amount) VALUES (nextval('order_id_seq'), %(item)s, %(amount)s)
# 2022-12-21 14:12:37,724 INFO sqlalchemy.engine.Engine [generated in 0.00027s] ({'item': 'Keypad', 'amount': 2000}, {'item': 'Laptop', 'amount': 15000}, {'item': 'GPU', 'amount': 10000}, {'item': 'Motherboard', 'amount': 9000}, {'item': 'CPU Cooler', 'amount': 7500})
# 2022-12-21 14:12:37,725 INFO sqlalchemy.engine.Engine COMMIT

print("menutup sesi transaction/koneksi ke database")
# bertujuan untuk menutup sesi transaction/koneksi ke database
session.close()
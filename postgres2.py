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

# return_defaults=True berarti SQL yang dihasilkan SQLAlchemy akan meng-return ID
print("masukkan banyak data ke dalam tabel database customer dalam 1 line code, dengan return_defaults=True")
session.bulk_save_objects([new_customer, new_customer1, new_customer2,
             new_customer3, new_customer4], return_defaults=True)
session.commit()

# 2022-12-21 11:35:18,141 INFO sqlalchemy.engine.Engine BEGIN (implicit)
# 2022-12-21 11:35:18,147 INFO sqlalchemy.engine.Engine INSERT INTO customer (id, first_name, last_name, age, country) VALUES (nextval('customer_id_seq'), %(first_name)s, %(last_name)s, %(age)s, %(country)s) RETURNING customer.id
# 2022-12-21 11:35:18,147 INFO sqlalchemy.engine.Engine [generated in 0.00095s] ({'first_name': 'John', 'last_name': 'Doe', 'age': 31, 'country': 'USA'}, {'first_name': 'Robert', 'last_name': 
# 'Luna', 'age': 22, 'country': 'USA'}, {'first_name': 'David', 'last_name': 'Robinson', 'age': 22, 'country': 'UK'}, {'first_name': 'John', 'last_name': 'Reinhardt', 'age': 25, 'country': 'UK'}, {'first_name': 'Betty', 'last_name': 'Doe', 'age': 28, 'country': 'UAE'})
# 2022-12-21 11:35:18,155 INFO sqlalchemy.engine.Engine COMMIT


# return_defaults=False berarti SQL yang dihasilkan SQLAlchemy tidak akan meng-return ID
print("masukkan banyak data ke dalam tabel database customer dalam 1 line code, dengan return_defaults=False")
session.bulk_save_objects([new_customer, new_customer1, new_customer2,
             new_customer3, new_customer4], return_defaults=False)
session.commit()

# 2022-12-21 11:35:18,155 INFO sqlalchemy.engine.Engine BEGIN (implicit)
# 2022-12-21 11:35:18,155 INFO sqlalchemy.engine.Engine UPDATE customer SET first_name=%(first_name)s, last_name=%(last_name)s, age=%(age)s, country=%(country)s WHERE customer.id = %(customer_id)s
# 2022-12-21 11:35:18,163 INFO sqlalchemy.engine.Engine [generated in 0.00139s] ({'first_name': 'John', 'last_name': 'Doe', 'age': 31, 'country': 'USA', 'customer_id': 146}, {'first_name': 'Robert', 'last_name': 'Luna', 'age': 22, 'country': 'USA', 'customer_id': 147}, {'first_name': 'David', 'last_name': 'Robinson', 'age': 22, 'country': 'UK', 'customer_id': 148}, {'first_name': 'John', 'last_name': 'Reinhardt', 'age': 25, 'country': 'UK', 'customer_id': 149}, {'first_name': 'Betty', 'last_name': 'Doe', 'age': 28, 'country': 'UAE', 'customer_id': 150})
# 2022-12-21 11:35:18,163 INFO sqlalchemy.engine.Engine COMMIT

print("insert multiple data ke dalam order")
new_order1 = Order(item='Keyboard', amount=400, customer_id=new_customer3.id)
new_order2 = Order(item='Mouse', amount=300, customer_id=new_customer3.id)
new_order3= Order(item='Monitor', amount=12000, customer_id=new_customer2.id)
new_order4 = Order(item='Keyboard', amount=400, customer_id=new_customer.id)
new_order5 = Order(item='Mousepad', amount=250, customer_id=new_customer1.id)

print("masukkan banyak data ke dalam tabel database order dalam 1 line code")
session.bulk_save_objects([new_order1, new_order2, new_order3, new_order4, new_order5])
session.commit()

# 2022-12-21 11:35:18,163 INFO sqlalchemy.engine.Engine BEGIN (implicit)
# 2022-12-21 11:35:18,171 INFO sqlalchemy.engine.Engine INSERT INTO "order" (id, item, amount, customer_id) VALUES (nextval('order_id_seq'), %(item)s, %(amount)s, %(customer_id)s)
# 2022-12-21 11:35:18,171 INFO sqlalchemy.engine.Engine [generated in 0.00091s] ({'item': 'Keyboard', 'amount': 400, 'customer_id': 149}, {'item': 'Mouse', 'amount': 300, 'customer_id': 149}, 
# {'item': 'Monitor', 'amount': 12000, 'customer_id': 148}, {'item': 'Keyboard', 'amount': 400, 'customer_id': 146}, {'item': 'Mousepad', 'amount': 250, 'customer_id': 147})
# 2022-12-21 11:35:18,171 INFO sqlalchemy.engine.Engine COMMIT

print("engine execute")
engine.execute("insert into customer (id, first_name, last_name, age, country) values (6, 'Setip', 'Cengiri', 7, 'IDN')")

# 2022-12-21 11:35:18,179 INFO sqlalchemy.engine.Engine insert into customer (id, first_name, last_name, age, country) values (6, 'Setip', 'Cengiri', 7, 'IDN')
# 2022-12-21 11:35:18,179 INFO sqlalchemy.engine.Engine [raw sql] {}
# 2022-12-21 11:35:18,179 INFO sqlalchemy.engine.Engine COMMIT

print("menutup sesi transaction/koneksi ke database")
# bertujuan untuk menutup sesi transaction/koneksi ke database
session.close()
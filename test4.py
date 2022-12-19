from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, CHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import delete
from sqlalchemy import update

Base = declarative_base()

class Product(Base):
    __tablename__ = "product"
    id = Column("id", Integer, primary_key=True)
    item = Column("item", String)
    price = Column("price", Integer)

    def __init__(self, id, item, price):
        self.id = id
        self.item = item
        self.price = price

    def __repr__(self):
        return f"({self.id}) {self.item} {self.price}" 

engine = create_engine("sqlite:///mydb.db", echo=True)

Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()

print("Proses delete data")
a = session.query(Product).filter(Product.id > 0).delete()
session.commit()

# 2022-12-19 13:44:10,572 INFO sqlalchemy.engine.Engine BEGIN (implicit)
# 2022-12-19 13:44:10,573 INFO sqlalchemy.engine.Engine DELETE FROM product WHERE product.id > ? 
# 2022-12-19 13:44:10,574 INFO sqlalchemy.engine.Engine [generated in 0.00044s] (0,)
# 2022-12-19 13:44:10,581 INFO sqlalchemy.engine.Engine COMMIT

print("Proses insert 5 data")
a1 = Product(1, "Keyboard", 400)
a2 = Product(2, "Mouse", 300)
a3 = Product(3, "Monitor", 12000)
a4 = Product(4, "Keyboard", 400)
a5 = Product(5, "Mousepad", 250)
session.add(a1)
session.add(a2)
session.add(a3)
session.add(a4)
session.add(a5)
session.commit()

# 2022-12-19 13:44:10,589 INFO sqlalchemy.engine.Engine BEGIN (implicit)
# 2022-12-19 13:44:10,591 INFO sqlalchemy.engine.Engine INSERT INTO product (id, item, price) VALUES (?, ?, ?)
# 2022-12-19 13:44:10,591 INFO sqlalchemy.engine.Engine [generated in 0.00043s] ((1, 'Keyboard', 
# 400), (2, 'Mouse', 300), (3, 'Monitor', 12000), (4, 'Keyboard', 400), (5, 'Mousepad', 250))    
# 2022-12-19 13:44:10,593 INFO sqlalchemy.engine.Engine COMMIT

print("query dan lakukan update")
result = session.query(Product).filter(Product.price == 400)
for input in result:
    print(input)
    input.item = "Processor"
session.commit()

# 2022-12-19 13:44:10,601 INFO sqlalchemy.engine.Engine BEGIN (implicit)
# 2022-12-19 13:44:10,603 INFO sqlalchemy.engine.Engine SELECT product.id AS product_id, product.item AS product_item, product.price AS product_price
# FROM product
# WHERE product.price = ?
# 2022-12-19 13:44:10,604 INFO sqlalchemy.engine.Engine [generated in 0.00102s] (400,)
# (1) Keyboard 400
# (4) Keyboard 400
# 2022-12-19 13:44:10,607 INFO sqlalchemy.engine.Engine UPDATE product SET item=? WHERE product.id = ?
# 2022-12-19 13:44:10,607 INFO sqlalchemy.engine.Engine [generated in 0.00047s] (('Processor', 1), ('Processor', 4))
# 2022-12-19 13:44:10,609 INFO sqlalchemy.engine.Engine COMMIT

print("query dengan id lebih dari 0")
output = session.query(Product).filter(Product.id > 0)
for data in output:
    print(data)

# 2022-12-19 13:44:10,619 INFO sqlalchemy.engine.Engine BEGIN (implicit)
# 2022-12-19 13:44:10,620 INFO sqlalchemy.engine.Engine SELECT product.id AS product_id, product.item AS product_item, product.price AS product_price
# FROM product
# WHERE product.id > ?
# 2022-12-19 13:44:10,621 INFO sqlalchemy.engine.Engine [generated in 0.00131s] (0,)
# (1) Processor 400
# (2) Mouse 300
# (3) Monitor 12000
# (4) Processor 400
# (5) Mousepad 250
# Hari ini mempelajari tentang primary_key, operator like(), dan membuat tabel database
#  secara otomatis menggunakan SQLAlchemy di Python (tidak manual seperti insert into, 
#   create table, dsb)


from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, CHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import delete

# Membuat sebuah class declarative base 
Base = declarative_base()


# Mendefinsikan tabel dengan nama "people" menggunakan class
class Person(Base):
    __tablename__ = "people"

    # "primary_key=True" bertujuan agar kolom tersebut hanya berisi data yang unik (tidak boleh ada yang sama)
    ssn = Column("ssn", Integer, primary_key=True)
    firstname = Column("firstname", String)
    lastname = Column("lastname", String)
    gender = Column("gender", CHAR)
    age = Column("age", Integer)

    def __init__(self, ssn, first, last, gender, age):
        self.ssn = ssn
        self.firstname = first
        self.lastname = last
        self.gender = gender
        self.age = age

    def __repr__(self):
        return f"({self.ssn}) {self.firstname} {self.lastname} {self.gender} {self.age}"

# Membuat sebuah koneksi ke database SQLite (create a connection to the SQLite database)
engine = create_engine("sqlite:///mydb.db", echo=True)

# Membuat tabel "people" di database (create the "people" table in the database)
Base.metadata.create_all(bind=engine)

# Membuat sebuah session untuk berinteraksi dengan database (create a session to interact with the database)
Session = sessionmaker(bind=engine)
session = Session()

# Bertujuan untuk menghapus data di tabel yang "ssn" nya lebih dari 0
x = session.query(Person).filter(Person.ssn > 0).\
    delete()
session.commit()

# Masukkan data yang ingin dimasukkkan pada tabel database, lalu di commit 
person = Person(12312, "Mike", "Smith", "m", 35)
session.add(person)
session.commit()

# Masukkan data yang ingin dimasukkan pada tabel databse, lalu di commit 
p1 = Person(31234, "Anna", "Blue", "f", 40)
p2 = Person(32423, "Bob", "Blue", "m", 35)
p3 = Person(45654, "Angela", "Cold", "f", 22)
session.add(p1)
session.add(p2)
session.add(p3)
session.commit()

# Query database untuk mengambil data yang diinginkan dari tabel "people"
#  (dibawah ini bertujuan mencari data/kolom dalam "Person" yang firstname nya 
#    berisi awalan 'A' dan akhiran 'a')
results = session.query(Person).filter(Person.firstname.like("A%a"))
for r in results:
    print(r)

# Operator like() bertujuan untuk mencari pola tertentu dalam kolom,
#  contoh-contoh lainnya dapat kunjungi: https://www.geeksforgeeks.org/python-mysql-like-operator/
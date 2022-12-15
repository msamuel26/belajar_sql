# Hari ini mempelajari tentang primary_key, operator like(), dan membuat tabel database
#  secara otomatis menggunakan SQLAlchemy di Python (tidak manual seperti insert into, 
#   create table, dsb)


from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, CHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import delete
from sqlalchemy import update 

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
print("[Proses delete]")
x = session.query(Person).filter(Person.ssn > 0).\
    delete()
session.commit()

# 2022-12-15 20:12:02,900 INFO sqlalchemy.engine.Engine BEGIN (implicit)
# 2022-12-15 20:12:02,901 INFO sqlalchemy.engine.Engine DELETE FROM people WHERE people.ssn > ?  
# 2022-12-15 20:12:02,901 INFO sqlalchemy.engine.Engine [generated in 0.00029s] (0,)
# 2022-12-15 20:12:02,903 INFO sqlalchemy.engine.Engine COMMIT


# Masukkan data yang ingin dimasukkkan pada tabel database, lalu di commit
print("[Insert 1 record]")
person = Person(12312, "Mike", "Smith", "m", 35)
session.add(person)
session.commit()

# 2022-12-15 20:12:02,911 INFO sqlalchemy.engine.Engine BEGIN (implicit)
# 2022-12-15 20:12:02,913 INFO sqlalchemy.engine.Engine INSERT INTO people (ssn, firstname, lastname, gender, age) VALUES (?, ?, ?, ?, ?)
# 2022-12-15 20:12:02,913 INFO sqlalchemy.engine.Engine [generated in 0.00063s] (12312, 'Mike', 'Smith', 'm', 35)
# 2022-12-15 20:12:02,915 INFO sqlalchemy.engine.Engine COMMIT

# Masukkan data yang ingin dimasukkan pada tabel databse, lalu di commit
print("[Insert 3 record]")
p1 = Person(31234, "Anna", "Blue", "f", 40)
p2 = Person(32423, "Bob", "Blue", "m", 35)
p3 = Person(45654, "Angela", "Cold", "f", 22)
session.add(p1)
session.add(p2)
session.add(p3)
session.commit()

# 2022-12-15 20:12:02,925 INFO sqlalchemy.engine.Engine BEGIN (implicit)
# 2022-12-15 20:12:02,925 INFO sqlalchemy.engine.Engine INSERT INTO people (ssn, firstname, lastname, gender, age) VALUES (?, ?, ?, ?, ?)
# 2022-12-15 20:12:02,926 INFO sqlalchemy.engine.Engine [generated in 0.00038s] ((31234, 'Anna', 
# 'Blue', 'f', 40), (32423, 'Bob', 'Blue', 'm', 35), (45654, 'Angela', 'Cold', 'f', 22))
# 2022-12-15 20:12:02,927 INFO sqlalchemy.engine.Engine COMMIT

# Query database untuk mengambil data yang diinginkan dari tabel "people"
#  (dibawah ini bertujuan mencari data/kolom dalam "Person" yang firstname nya 
#    berisi awalan 'A' dan akhiran 'a')
print("[update record dengan cara diquery dulu setelah itu diupdate]")
results = session.query(Person).filter(Person.firstname.like("A%a"))
for r in results:
    print(r)
    r.lastname='Empritu'
session.commit()

# 2022-12-15 20:12:02,936 INFO sqlalchemy.engine.Engine BEGIN (implicit)
# 2022-12-15 20:12:02,938 INFO sqlalchemy.engine.Engine SELECT people.ssn AS people_ssn, people.firstname AS people_firstname, people.lastname AS people_lastname, people.gender AS people_gender, people.age AS people_age
# FROM people
# WHERE people.firstname LIKE ?
# 2022-12-15 20:12:02,939 INFO sqlalchemy.engine.Engine [generated in 0.00056s] ('A%a',)
# (31234) Anna Blue f 40
# (45654) Angela Cold f 22
# 2022-12-15 20:12:02,941 INFO sqlalchemy.engine.Engine UPDATE people SET lastname=? WHERE people.ssn = ?
# 2022-12-15 20:12:02,941 INFO sqlalchemy.engine.Engine [generated in 0.00077s] (('Empritu', 31234), ('Empritu', 45654))
# 2022-12-15 20:12:02,943 INFO sqlalchemy.engine.Engine COMMIT

print("[update query yang ssn nya lebih dari 0]")
results = session.query(Person).filter(Person.ssn > 0)
for r in results:
    print(r)

# 2022-12-15 20:12:02,952 INFO sqlalchemy.engine.Engine BEGIN (implicit)
# 2022-12-15 20:12:02,953 INFO sqlalchemy.engine.Engine SELECT people.ssn AS people_ssn, people.firstname AS people_firstname, people.lastname AS people_lastname, people.gender AS people_gender, people.age AS people_age
# FROM people
# WHERE people.ssn > ?
# 2022-12-15 20:12:02,953 INFO sqlalchemy.engine.Engine [generated in 0.00072s] (0,)
# (12312) Mike Smith m 35
# (31234) Anna Empritu f 40
# (32423) Bob Blue m 35
# (45654) Angela Empritu f 22
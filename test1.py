from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Teman(Base):
    __tablename__ = "teman"
    id = Column("id", Integer, primary_key=True)
    nama = Column("nama", String)
    alamat = Column("alamat", String)
    
    def __init__(self, id, nama, alamat):
        self.id = id
        self.nama = nama
        self.alamat = alamat

    def __repr__(self):
        return f"({self.id}) {self.nama} {self.alamat}"

engine = create_engine("sqlite:///mydb.db", echo=True)

Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()

y = session.query(Teman).filter(Teman.id > 0).delete()
session.commit()

t1 = Teman(1, "Setip", "Jalan1")
t2 = Teman(2, "Cinguri", "Jalan2")
t3 = Teman(3, "Cengir", "Jalan3")
session.add(t1)
session.add(t2)
session.add(t3)
session.commit()

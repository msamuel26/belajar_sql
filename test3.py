from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, CHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import delete
from sqlalchemy import update

Base = declarative_base()

class Mapel(Base):
    __tablename__ = "mapel"
    id = Column("id", Integer, primary_key=True)
    nama_mapel = Column("nama_mapel", String)
    nama_guru = Column("nama_guru", String)
    asal = Column("asal", String)

    def __init__(self, id, nama_mapel, nama_guru, asal):
        self.id = id
        self.nama_mapel = nama_mapel
        self.nama_guru = nama_guru
        self.asal = asal

    def __repr__(self):
        return f"({self.id}) {self.nama_mapel} {self.nama_guru} {self.asal}"

engine = create_engine("sqlite:///mydb.db", echo=True)

Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()

print("[Proses delete (menghapus data)]")
i = session.query(Mapel).filter(Mapel.id > 0).delete()
session.commit()

# 2022-12-15 21:00:46,873 INFO sqlalchemy.engine.Engine BEGIN (implicit)
# 2022-12-15 21:00:46,874 INFO sqlalchemy.engine.Engine DELETE FROM mapel WHERE mapel.id > ?     
# 2022-12-15 21:00:46,874 INFO sqlalchemy.engine.Engine [generated in 0.00036s] (0,)
# 2022-12-15 21:00:46,880 INFO sqlalchemy.engine.Engine COMMIT

print("[Proses insert 3 data]")
i1 = Mapel(1, "Matematika", "Pak Budi", "Semarang")
i2 = Mapel(2, "IPA", "Pak Edo", "Bandung")
i3 = Mapel(3, "Bahasa Inggris", "Bu Siti", "Purwokerto")
session.add(i1)
session.add(i2)
session.add(i3)
session.commit()

# 2022-12-15 20:59:44,772 INFO sqlalchemy.engine.Engine BEGIN (implicit)
# 2022-12-15 20:59:44,774 INFO sqlalchemy.engine.Engine INSERT INTO mapel (id, nama_mapel, nama_guru, asal) VALUES (?, ?, ?, ?)
# 2022-12-15 20:59:44,774 INFO sqlalchemy.engine.Engine [generated in 0.00064s] ((1, 'Matematika', 'Pak Budi', 'Semarang'), (2, 'IPA', 'Pak Edo', 'Bandung'), (3, 'Bahasa Inggris', 'Bu Siti', 'Purwokerto'))
# 2022-12-15 20:59:44,778 INFO sqlalchemy.engine.Engine COMMIT

print("[query dengan like dan lakukan update]")
output = session.query(Mapel).filter(Mapel.nama_guru.like("Pak%"))
for data in output:
    print(data)
    data.asal = "Ungaran"
session.commit()

# 2022-12-15 21:04:25,069 INFO sqlalchemy.engine.Engine BEGIN (implicit)
# 2022-12-15 21:04:25,071 INFO sqlalchemy.engine.Engine SELECT mapel.id AS mapel_id, mapel.nama_mapel AS mapel_nama_mapel, mapel.nama_guru AS mapel_nama_guru, mapel.asal AS mapel_asal
# FROM mapel
# WHERE mapel.nama_guru LIKE ?
# 2022-12-15 21:04:25,072 INFO sqlalchemy.engine.Engine [generated in 0.00063s] ('Pak%',)        
# (1) Matematika Pak Budi Semarang
# (2) IPA Pak Edo Bandung
# 2022-12-15 21:04:25,075 INFO sqlalchemy.engine.Engine UPDATE mapel SET asal=? WHERE mapel.id = 
# ?
# 2022-12-15 21:04:25,075 INFO sqlalchemy.engine.Engine [generated in 0.00070s] (('Ungaran', 1), 
# ('Ungaran', 2))
# 2022-12-15 21:04:25,077 INFO sqlalchemy.engine.Engine COMMIT

print("[query dengan id lebih dari 0]")
output1 = session.query(Mapel).filter(Mapel.id > 0)
for a in output1:
    print(a)

# 2022-12-15 21:04:25,088 INFO sqlalchemy.engine.Engine BEGIN (implicit)
# 2022-12-15 21:04:25,089 INFO sqlalchemy.engine.Engine SELECT mapel.id AS mapel_id, mapel.nama_mapel AS mapel_nama_mapel, mapel.nama_guru AS mapel_nama_guru, mapel.asal AS mapel_asal
# FROM mapel
# WHERE mapel.id > ?
# 2022-12-15 21:04:25,089 INFO sqlalchemy.engine.Engine [generated in 0.00061s] (0,)
# (1) Matematika Pak Budi Ungaran
# (2) IPA Pak Edo Ungaran
# (3) Bahasa Inggris Bu Siti Purwokerto
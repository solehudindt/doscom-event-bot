from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker
# Kita harus import setiap tipe data yang ingin kita gunakan
from sqlalchemy import create_engine

engine = create_engine('mysql+mysqlconnector://admin:admin123@localhost:3306/bot_tele') 
Base = declarative_base()
# setiap class yang akan dipetakan harus inherit dari instance declarative_base

class Debot(Base): #inherit from Base
    __tablename__ = 'debot'    
    # tablename disini hanya sebagai metadata

    id = Column(Integer, nullable=False, primary_key=True)
    jenis = Column(String(8), nullable=False)
    nama = Column(String(25), nullable=False)
       
    tanggal = Column(Date, nullable=False)

    def __repr__(self):
    	return "<Debot(jenis='{0}', nama='{1}', tanggal='{2}')>".format(
    			self.jenis, self.nama, self.tanggal)

Base.metadata.create_all(engine) 
# # menjalankan perintah pemetaan/membuat database

DBSession = sessionmaker()
DBSession.configure(bind=engine)
session = DBSession()
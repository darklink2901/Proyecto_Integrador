import os
import csv

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

# engine = create_engine('postgres://rrjkyrln:ts_1CbU630y1vqHWrDyKTSiEkP6Go6GH@drona.db.elephantsql.com:5432/rrjkyrln')
engine = create_engine('postgresql://postgres:hernandez@localhost:5432/proyectoint')
# postgresql://postgres:hernandez@localhost:5432/proyectoint

db = scoped_session(sessionmaker(bind=engine))

def main():
    f = open("materiales.csv")
    reader = csv.reader(f)
    for idMaterial, nombre, precio, cantidad, area_id in reader:
        if(idMaterial != 'idMaterial'):
            db.execute("INSERT INTO ControlEscolar_material ( nombre, precio, cantidad, area_id) VALUES ( :nombre, :precio, :cantidad, :area_id)",{ "nombre": nombre, "precio": precio, "cantidad": cantidad, "area_id": area_id})
    db.commit()

if __name__ == "__main__":
    main()

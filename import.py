import csv
import os

from sqlalchemy import create_engine, Table, Column, String, Integer, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.getenv("DATABASE_URL"))
Session = scoped_session(sessionmaker(bind=engine))
db = Session()
meta = MetaData()

db.execute('CREATE TABLE "books2" ('
           'isbn VARCHAR NOT NULL, '
           'title VARCHAR NOT NULL, '
           'author VARCHAR NOT NULL, '
           'year INTEGER NOT NULL, '
           'PRIMARY KEY (isbn));'
           )
db.commit()

f=open("books.csv")
reader=csv.reader(f)
next(reader)
for isbn, title, author, year in reader:
    db.execute("INSERT INTO books2 (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)",
    {"isbn": isbn, "title": title, "author": author, "year": year})
    db.commit()
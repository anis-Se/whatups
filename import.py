import os
import csv
from application import db
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

"""
# Set up database
engine = create_engine("postgres://asfygvclmkybrf:948ff2d7e016b16180b1704de19a196f2f970cf6e1605f662e7b318d235b4553@ec2-54-247-78-30.eu-west-1.compute.amazonaws.com:5432/dd12dmrhhq8clj")
db = scoped_session(sessionmaker(bind=engine))
"""
engine = create_engine("postgres:///mydb")
db = scoped_session(sessionmaker(bind=engine))
def main():
	f=open("books.csv")
	reader = csv.reader(f)
	for isbn, title, author, year in reader:
		db.execute("INSERT INTO books (isbn, title, author, year)VALUES (:isbn, :title, :author, :year)",
			 {"isbn":isbn, "title":title, "author":author, "year":year})
		print("done.")
	db.commit()

if __name__ == "__main__":
    main()
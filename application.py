import os, json, requests
from flask_login import login_user, current_user, logout_user, login_required
from flask import Flask, request,session, url_for, render_template, redirect
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from forms import RegistrationForm, LogInForm, searchForm, reviewsForm

app = Flask(__name__)
"""
# Set up database
engine = create_engine("postgres://asfygvclmkybrf:948ff2d7e016b16180b1704de19a196f2f970cf6e1605f662e7b318d235b4553@ec2-54-247-78-30.eu-west-1.compute.amazonaws.com:5432/dd12dmrhhq8clj")
db = scoped_session(sessionmaker(bind=engine))
"""
engine = create_engine("postgres:///mydb")
db = scoped_session(sessionmaker(bind=engine))
# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SECRET_KEY"]='a0338eb210d334ead02d1eb64a281c2a'
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

notes= []
@app.route("/")
def index():
	if not session["user_id"] :
		return render_template("index.html")
	return redirect(url_for('search'))
	

@app.route("/register", methods=['GET', 'POST'])
def register():
	if session["user_id"] == [] :

		form = RegistrationForm()
		if form.validate_on_submit():
			if request.method == "POST":
				username = request.form.get("username")
				password = request.form.get("password")
				email = request.form.get("email")
				db.execute("INSERT INTO users (username, password, email) VALUES (:username, :password, :email)", {"username": username, "password": password, "email": email})
				#db.session.add(user)
				db.commit()
				return render_template("succes.html")
		return render_template("register.html", form=form)
	return redirect(url_for('search'))
@app.route("/login", methods=['GET', 'POST'])
def login():
	if session["user_id"] == [] :
		form = LogInForm()
		if form.validate_on_submit():
			if request.method == "POST":
				username = request.form.get("username")
				password = request.form.get("password")
				name = db.execute("SELECT * FROM users").fetchall()
				session["user_id"]=[]
				for u in name:
					if str(u.username) == username and str(u.password) == password:
						a = u.id
						session["user_id"].append(a)	
						return redirect(url_for('search'))
				
		return render_template("login.html", form=form)
	return redirect(url_for('search'))

@app.route("/logout")
def logout():
	session["user_id"] = 0
	return redirect(url_for('index'))

@app.route("/forgotpassword", methods=['GET', 'POST'])
def forgotpassword():
    return render_template("forgotpassword.html")


@app.route("/search", methods=['GET', 'POST'])
def search():
	if session["user_id"] != [] :
		form = searchForm()
		if form.validate_on_submit():
			if request.method == "POST":
				a=[]
				sear = request.form.get ("bbar")
				books = db.execute("SELECT * FROM books").fetchall()
				for b in books :
					if sear == b.isbn :
						a.append(b)
						c= b.isbn
						notes.append(b.isbn)
						return render_template('book.html', b=a)
					elif  sear in b.author or sear in b.title  :
						a.append(b)
						c = b.isbn
						
				return render_template('book.html', b=a)
				
		return render_template("search.html", form=form, user_id=session["user_id"])
	return redirect(url_for('login'))

@app.route("/books/<isbn>")
def books(isbn):
	if session["user_id"] != 0 :
		
		a=[]
		books = db.execute("SELECT * FROM books").fetchall()
		for b in books :
			if isbn == b.isbn :
				notes.append(b.isbn)
				c = isbn
				a.append(b)
				d = []
				res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "O3uUGINbJ8F868fosT5A", "isbns":isbn})
				if res.status_code != 200:
						raise Exception("ERROR: API request unsuccessful.")
				ress = res.json()
				#r=ress["title"]
				review = db.execute("SELECT * FROM reviews").fetchall()
				for rev in review:
					if rev.u_books == c :
						d.append(rev)

						#return render_template('books.html', b=a, d=d)
				return render_template('books.html', b=a, d=d)
		return render_template("error.html", message="No such book.")
	return redirect(url_for('login'))


@app.route("/reviews/<isbn>", methods=['POST', 'GET'])
def reviews(isbn):
	if session["user_id"] != [] :
		form = reviewsForm()
		if request.method == "POST":
			comment = request.form.get("comment")
			[user_id] = session["user_id"]
			#u_books = notes[0]
			u_books=isbn
			db.execute("INSERT INTO reviews (user_id, u_books, comment) VALUES (:user_id, :u_books, :comment)", {"user_id": user_id, "u_books": u_books, "comment": comment})
			db.commit()
			return redirect(url_for('books', isbn=isbn))

		return render_template('reviews.html', form=form,b=isbn)
	return redirect(url_for('login'))

@app.route("/api/<isbn>", methods=['GET'])
def api(isbn):
	if session["user_id"] != 0 :
		books = db.execute("SELECT * FROM books").fetchall()
		for b in books :
			if isbn == b.isbn :
				res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "O3uUGINbJ8F868fosT5A", "isbns":isbn})
				if res.status_code != 200:
					raise Exception("ERROR: API request unsuccessful.")
				ress = res.json()
				return ress
				#return render_template('api.html', ress=ress)
	return redirect(url_for('login'))

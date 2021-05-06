import os
import requests
import json

from flask import Flask, session, render_template, request, redirect, url_for, jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variablez
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
Session = scoped_session(sessionmaker(bind=engine))
db = Session()

# App Routes
@app.route("/")
def home():
    if session.get("user") is None:
        return render_template("home.html", authorized=False)
    else:
        return render_template("home.html", authorized=True, username=session["user"])


@app.route("/register")
def register():
    if session.get("user") is not None:
        return render_template("error.html", error="You are already logged in! You don't need to register.")
    else:
        return render_template("register.html")


@app.route("/register_process", methods=["GET", "POST"])
def register_process():
    if request.method == "GET":
        return render_template("error.html", error="It looks like you can't visit this web page!")
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        if db.execute("SELECT * FROM users WHERE username = :username", {"username": username}).rowcount == 1:
            return render_template("error.html", error="This username is already taken by somebody else.")
        else:
            db.execute("INSERT INTO users (username, password) VALUES (:username, :password)", {
                       "username": username, "password": password})
            db.commit()
            session["user"] = username
            return redirect("/")


@app.route("/login")
def login():
    if session.get("user") is not None:
        return render_template("error.html", error="You are already logged in!.")
    else:
        return render_template("login.html")


@app.route("/login_process", methods=["GET", "POST"])
def login_process():
    if request.method == "GET":
        return render_template("error.html", error="It looks like you can't visit this web page!")
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        if db.execute("SELECT * FROM users WHERE username = :username AND password = :password", {"username": username, "password": password}).rowcount == 1:
            session["user"] = username
            return redirect(url_for("home"))
        else:
            return render_template("error.html", error="Username or password is incorrect!")


@app.route("/logout")
def logout():
    session["user"] = None
    return redirect(url_for("home"))


@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "GET":
        return render_template("error.html", error="It looks like you can't visit this web page!")
    else:
        search = request.form.get("search")
        result = db.execute("SELECT * FROM books WHERE (isbn LIKE :search) OR (title LIKE :search) OR (author LIKE :search)",
                            {"search": '%' + search + '%'})
        if result.rowcount == 0:
            return render_template("error.html", error="No such book has been found!")
        else:
            return render_template("search.html", result=result)


@app.route("/book_page")
def no_isbn():
    return render_template("error.html", error="Please, specify ISBN.")


@app.route("/book_page/<string:isbn>")
def book_page(isbn):
    # Check if user is logged in
    if session.get("user") == None:
        return render_template("error.html", error="It looks like you can't visit this web page!")
    else:
        # Check if the book exist
        if db.execute("SELECT * FROM books WHERE isbn = :isbn", {"isbn": isbn}).rowcount == 0:
            return render_template("error.html", error="No such book has been found!")
        else:
            # Get book info
            book_info = db.execute(
                "SELECT * FROM books WHERE isbn = :isbn", {"isbn": isbn}).fetchone()
            # Get reviews
            if db.execute("SELECT * FROM reviews WHERE isbn = :isbn", {"isbn": isbn}).rowcount == 0:
                reviews = False
            else:
                reviews = db.execute(
                    "SELECT * FROM reviews WHERE isbn = :isbn", {"isbn": isbn})
            # Get GoodBook rating
            if db.execute("SELECT rating FROM reviews WHERE isbn = :isbn", {"isbn": isbn}).rowcount == 0:
                goodbook_rating = None
            else:
                rating_avg = db.execute("SELECT AVG (rating) FROM reviews WHERE isbn = :isbn", {
                    "isbn": isbn}).fetchone()
                goodbook_rating = round(rating_avg[0], 2)
            # get number of reviews on GoodBook
            ratings_count = db.execute(
                "SELECT COUNT (rating) FROM reviews WHERE isbn = :isbn", {"isbn": isbn}).fetchone()
            goodbook_work_ratings_count = int(ratings_count[0])
            # Get GoodReads rating
            res = requests.get("https://www.goodreads.com/book/review_counts.json",
                               params={"key": "VFZamR1gadphxtnZCZilA", "isbns": isbn})
            data = res.json()
            goodreads_rating = float(data["books"][0]["average_rating"])
            # Get number of reviews on GoodReads
            goodreads_work_ratings_count = int(
                data["books"][0]["work_ratings_count"])
            # Check if user already left a review
            if db.execute("SELECT * FROM reviews WHERE isbn = :isbn AND username = :username", {"isbn": isbn, "username": session["user"]}).rowcount == 1:
                print(goodbook_work_ratings_count)
                return render_template("book_page.html", book=book_info, reviews=reviews, goodbook_rating=goodbook_rating, goodbook_work_ratings_count=goodbook_work_ratings_count, goodreads_rating=goodreads_rating, goodreads_work_ratings_count=goodreads_work_ratings_count, add_review=False)
            else:
                return render_template("book_page.html", book=book_info, reviews=reviews, goodbook_rating=goodbook_rating, goodbook_work_ratings_count=goodbook_work_ratings_count, goodreads_rating=goodreads_rating, goodreads_work_ratings_count=goodreads_work_ratings_count, add_review=True)


@app.route("/book_page/<string:isbn>/add_review", methods=["GET", "POST"])
def add_review(isbn):
    if request.method == "GET":
        return render_template("error.html", error="It looks like you can't visit this web page!")
    else:
        isbn = isbn
        username = session["user"]
        rating = request.form.get("rating")
        review = request.form.get("review")
        db.execute("INSERT INTO reviews (isbn, username, rating, review) VALUES (:isbn, :username, :rating, :review)",
                   {"isbn": isbn, "username": username, "rating": rating, "review": review})
        db.commit()
        return redirect(f"/book_page/{isbn}")


@app.route("/api/<string:isbn>")
def api(isbn):
    if db.execute("SELECT * FROM reviews WHERE isbn = :isbn", {"isbn": isbn}).rowcount == 0:
        return "<h1>Error</h1><h2>The reasons why you might see this page: <ul><li>You might typed in incorrect ISBN</li><li>We don't have any data about this book</li>"
    else:
        book = db.execute(
            "SELECT * FROM books WHERE isbn = :isbn", {"isbn": isbn}).fetchone()
        rating_avg = db.execute("SELECT AVG (rating) FROM reviews WHERE isbn = :isbn", {
                                "isbn": isbn}).fetchone()
        rating = float(round(rating_avg[0], 2))
        ratings_count = db.execute(
            "SELECT COUNT (rating) FROM reviews WHERE isbn = :isbn", {"isbn": isbn}).fetchone()
        review_count = int(ratings_count[0])
        return jsonify({
            "title": book.title,
            "author": book.author,
            "year": book.year,
            "isbn": book.isbn,
            "review_count": review_count,
            "average_score": rating
        })

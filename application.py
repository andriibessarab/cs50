import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    # Get user's cash
    usr_cash = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=session["user_id"])[0]["cash"]

    # Get user's current stocks
    rows = db.execute("SELECT symbol, shares FROM curr_stocks WHERE user_id = :user_id", user_id=session["user_id"])

    # Count user's total cash(including purchased stocks)
    total = usr_cash

    for row in rows:

        # Call lookup function
        info = lookup(row["symbol"])

        # Remember this stock's name, price, and total
        row["name"] = info["name"]
        row["price"] = info["price"]
        row["total"] = info["price"] * row["shares"]

        # Add curr. stock's shares' price to total
        total += row["total"]

    # Render template with information above
    return render_template("index.html", rows=rows, cash=usr_cash, total=total)


@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    """Add money to account"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Request form
        cash = request.form.get("cash")

        # Ensure money was submitted
        if not cash.replace(" ", ""):
            return apology("must provide cash", 403)

        # Convert cash to integer
        cash = int(cash)

        # Ensure money is positive integer
        if cash < 1:
            return apology("cash must be a positive integer", 403)

        # Get user's cash
        usr_cash = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=session["user_id"])[0]["cash"]

        # Add money to user's account
        db.execute("UPDATE users SET cash = :cash WHERE id = :user_id", cash=usr_cash+cash, user_id=session["user_id"])

        # Redirect user to homepage
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("add.html")


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Request form
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        # Ensure symbol was submitted
        if not symbol.replace(" ", ""):
            return apology("must provide symbol", 403)

        # Ensure number of shares was submitted
        if not shares.replace(" ", ""):
            return apology("must provide number of shares", 403)

        # Convert shares to integer
        shares = int(shares)

        # Ensure shares is positive integer
        if shares < 1:
            return apology("shares must be a positive integer", 403)

        # Call lookup function
        info = lookup(symbol)

        # Ensure result is not None
        if not info:
            return apology("incorrect symbol", 403)

        # Get user's cash
        usr_cash = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=session["user_id"])[0]["cash"]

        # Calculate how much user needs
        total = info["price"] * shares

        # Ensure user has enough cash
        if usr_cash < total:
            return apology("not enough money", 403)

        # Subtract money from user's account
        db.execute("UPDATE users SET cash = :cash WHERE id = :user_id", cash=usr_cash-total, user_id=session["user_id"])

        # Add to curr_stocks table
        if db.execute("SELECT * FROM curr_stocks WHERE user_id = :user_id AND symbol = :symbol", user_id=session["user_id"], symbol=symbol):
            usr_shares = db.execute("SELECT shares FROM curr_stocks WHERE user_id = :user_id AND symbol = :symbol",
                                    user_id=session["user_id"], symbol=symbol)
            db.execute("UPDATE curr_stocks SET shares = :shares WHERE user_id = :user_id AND symbol = :symbol",
                       shares=usr_shares+shares, user_id=session["user_id"], symbol=symbol)
        else:
            db.execute("INSERT INTO curr_stocks (user_id, symbol, shares) VALUES (:user_id, :symbol, :shares)",
                       user_id=session["user_id"], symbol=symbol, shares=shares)

        # Record transaction
        db.execute("INSERT INTO transactions (user_id, symbol, shares, price) VALUES (:user_id, :symbol, :shares, :price)",
                   user_id=session["user_id"], symbol=symbol, shares=shares, price=info["price"])

        # Redirect user to homepage
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    # Get all user's transactions
    transactions = db.execute(
        "SELECT symbol, shares, price, transacted FROM transactions WHERE user_id = :user_id", user_id=session["user_id"])

    # Return a template with information above
    return render_template("history.html", transactions=transactions)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Request form
        username = request.form.get("username")
        password = request.form.get("password")

        # Ensure username was submitted
        if not username.replace(" ", ""):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not password.replace(" ", ""):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=username)

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to homepage
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/login")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Request form
        symbol = request.form.get("symbol")

        # Ensure symbol was submitted
        if not symbol.replace(" ", ""):
            return apology("must provide symbol", 403)

        # Call lookup function
        info = lookup(symbol)

        # Ensure result is not None
        if not info:
            return apology("incorrect symbol", 403)

        # Show result with information above
        return render_template("quoted.html", company=info["name"], symbol=info["symbol"], price=info["price"])

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Request form
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Ensure username was submitted
        if not username.replace(" ", ""):
            return apology("must provide username", 403)

        # Ensure password was submitted
        if not password.replace(" ", ""):
            return apology("must provide password", 403)

        # Ensure confirmation was submitted
        if not confirmation.replace(" ", ""):
            return apology("must confirm password", 403)

        # Ensure username is available
        if db.execute("SELECT username FROM users WHERE username = :username", username=username):
            return apology("username is taken", 403)

        # Ensure password and confirmation matches
        if password != confirmation:
            return apology("passwords didn't match", 403)

        # Add user to database
        db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash)",
                   username=username, hash=generate_password_hash(password))

        # Redirect to login form
        return redirect("/login")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Request form
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        # Ensure symbol was submitted
        if not symbol:
            return apology("must provide symbol", 403)

        # Ensure number of shares was submitted
        if not shares.replace(" ", ""):
            return apology("must provide number of shares", 403)

        # Convert shares to integer
        shares = int(shares)

        # Ensure shares is positive integer
        if shares < 1:
            return apology("shares must be a positive integer", 403)

        # Call lookup function
        info = lookup(symbol)

        # Ensure result is not None
        if not info:
            return apology("incorrect symbol", 403)

        # Get user's current number of shares
        usr_shares = db.execute("SELECT shares FROM curr_stocks WHERE user_id = :user_id AND symbol = :symbol",
                                user_id=session["user_id"], symbol=symbol)

        if usr_shares:
            usr_shares = usr_shares[0]["shares"]
        else:
            usr_shares = 0

        # Ensure user has enough shares
        if not usr_shares or usr_shares < shares:
            return apology("not enought shares", 403)

        # Calculate how much user will earn
        total = info["price"] * shares

        # Get user's cash
        usr_cash = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=session["user_id"])[0]["cash"]

        # Add money to user's account
        db.execute("UPDATE users SET cash = :cash WHERE id=:user_id", cash=usr_cash+total, user_id=session["user_id"])

        # Subtract/Remove from curr_stocks table
        if db.execute("SELECT shares FROM curr_stocks WHERE user_id = :user_id AND symbol = :symbol", user_id=session["user_id"], symbol=symbol)[0]["shares"] == shares:
            db.execute("DELETE FROM curr_stocks WHERE user_id = :user_id AND symbol = :symbol",
                       user_id=session["user_id"], symbol=symbol)
        else:
            db.execute("UPDATE curr_stocks SET shares = :shares WHERE user_id = :user_id AND symbol = :symbol",
                       shares=usr_shares-shares, user_id=session["user_id"], symbol=symbol)

        # Record transaction
        db.execute("INSERT INTO transactions (user_id, symbol, shares, price) VALUES (:user_id, :symbol, :shares, :price)",
                   user_id=session["user_id"], symbol=symbol, shares=shares/-1, price=info["price"])

        # Redirect user to homepage
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:

        # Get symbols
        symbols = db.execute("SELECT symbol FROM curr_stocks WHERE user_id = :user_id", user_id=session["user_id"])

        return render_template("sell.html", symbols=symbols)


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

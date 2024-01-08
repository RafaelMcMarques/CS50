import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    # get a dict with all user's stocks
    symbols = db.execute("SELECT DISTINCT(symbol) FROM transactions WHERE user_id = ?", session["user_id"])
    cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]

    # user has no stocks
    if not symbols:
        return render_template("index.html",value=usd(0), cash=usd(cash), total = usd(0 + cash) )

    stocks = []
    for symbol in symbols :
        stock = {}
        stock["symbol"] = symbol["symbol"]
        bought =  db.execute("SELECT SUM(shares) FROM transactions WHERE user_id = ? AND symbol = ? AND type = ?", session["user_id"], symbol["symbol"], "BUY")[0]["SUM(shares)"]
        sold = db.execute("SELECT SUM(shares) FROM TRANSACTIONS WHERE user_id = ? AND symbol = ? AND type = ?", session["user_id"], symbol["symbol"], "SELL")[0]["SUM(shares)"]
        if not sold:
            sold = 0
        stock["shares"] = bought - sold
        stock["price"] = lookup(symbol["symbol"])["price"]
        stock["total"] = stock["price"] * stock["shares"]
        stock["price"] = usd(stock["price"])
        stocks.append(stock)

    #get portfolio's value and user's cash
    value = 0
    for stock in stocks :
        value += stock["total"]
        stock["total"] = usd(stock["total"])

    return render_template("index.html", stocks=stocks, value=usd(value), cash=usd(cash), total = usd(value + cash))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    if request.method == "GET" :
        return render_template("buy.html")

    if not request.form.get("symbol") or not request.form.get("shares") :
        return apology("All fields required")

    # validate input
    symbol = request.form.get("symbol")
    shares = request.form.get("shares")
    if not shares.isdigit() or int(shares) < 0 :
        return apology("Invalid number of shares")

    # get stock
    stock = lookup(symbol)
    if not stock :
        return apology("Invalid symbol")

    # validate and update user's cash
    userData = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
    userData = userData[0]
    if int(userData["cash"]) - stock["price"] * int(shares) < 0 :
        return apology("Not enough cash")
    userData["cash"] -= stock["price"] * int(shares)

    # update database
    db.execute("INSERT INTO transactions (user_id, symbol, shares, price, type) VALUES (?,?,?,?,?)", session["user_id"], symbol, shares, stock["price"], "BUY")
    db.execute("UPDATE users SET cash = ? WHERE id = ?", userData["cash"], userData["id"])

    return redirect("/")



@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    transactions = db.execute("SELECT * FROM transactions WHERE user_id = ? ORDER BY Timestamp ASC", session["user_id"])
    return render_template("history.html", transactions=transactions)



@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
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
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "GET" :
        return render_template("quote.html")

    if not request.form.get("symbol") :
        return apology("Must provide symbol")
    symbol = request.form.get("symbol")
    stock = {}
    stock = lookup(symbol)
    if not stock :
        return apology("Not found")

    stock["price"]= usd(stock["price"])
    return render_template("quote.html", stock=stock)



@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET" :
        return render_template("register.html")

    if not request.form.get("username") or not request.form.get("password") or not request.form.get("confirmation") :
        return apology("All fields required")

    username = request.form.get("username")
    password1 = request.form.get("password")
    password2 = request.form.get("confirmation")

    if password1 != password2 :
        return apology("Passwords don't match")
    if db.execute("SELECT * FROM users WHERE username = ?", username) :
        return apology("Username unavailable")

    db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, generate_password_hash(password1))
    return redirect("/login")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    if request.method == "GET" :
        symbols = db.execute("SELECT DISTINCT(symbol) FROM transactions WHERE user_id = ?", session["user_id"])
        return render_template("sell.html", symbols=symbols)

    # validate input
    if not request.form.get("symbol") or not request.form.get("shares") :
        return apology("All fields required")
    if not request.form.get("shares").isdigit():
        return apology("Invalid number")
    symbol = request.form.get("symbol")
    shares = request.form.get("shares")

    # check if operation is possible
    bought = db.execute("SELECT SUM(shares) FROM transactions WHERE user_id = ? AND symbol = ? AND type = ?", session["user_id"], symbol, "BUY")[0]["SUM(shares)"]
    sold = db.execute("SELECT SUM(shares) FROM transactions WHERE user_id = ? AND symbol = ? AND type = ?", session["user_id"], symbol, "SELL")[0]["SUM(shares)"]
    if not sold :
        sold = 0
    owned = bought - sold
    if owned < int(shares) :
        return apology("Invalid quantity")

    # update database
    value = lookup(symbol)["price"]
    total = value * int(shares)
    cash = db.execute("SELECT cash FROM users WHERE id = ? ", session["user_id"])[0]["cash"] + total
    db.execute("INSERT INTO transactions (user_id, symbol, shares, price, type) VALUES (?,?,?,?,?)", session["user_id"], symbol, shares, value, "SELL")
    db.execute("UPDATE users SET cash = ? WHERE id = ?", cash, session["user_id"])
    return redirect("/")

@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    if request.method == "GET" :
        return redirect("/")

    if not request.form.get("amount") :
        return redirect("/")

    amount = request.form.get("amount")
    if not amount.isdigit() or int(amount) <= 0 :
        return apology("Invalid amount")

    cash = int(db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]) + int(amount)
    db.execute("UPDATE users SET cash = ? WHERE id = ?", cash, session["user_id"])
    return redirect("/")











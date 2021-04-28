
from dotenv import load_dotenv  # use dotenv to hide the sensitive information
from flask import Flask, render_template, request, jsonify, redirect, flash, session, send_from_directory
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, ShoppingList, UserFav

import os
import json
import requests

from forms import LoginForm, RegisterForm, AsinSearchForm, ReviewsByAsinForm, ShoppingListForm

app = Flask(__name__)

# connect database
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL', "postgres:///truedeal")
# compress the warning
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# echo the sql command
app.config['SQLALCHEMY_ECHO'] = True
# CONFIG THE DEBUGTOOL
app.debug = True
# config heroku variable, secret key
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'YOUDONTKNOWTHAT')
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['TEMPLATES_AUTO_RELOAD'] = True

#toolbar = DebugToolbarExtension(app)

# connect the app, database
connect_db(app)
# create table
db.create_all()


# api key, hide the key in env
load_dotenv()
key = os.getenv("AMAZON_REQUEST_KEY")


# function to search

def request_amazon(amazonkeyword, country):
    """this will return json for the product keyword"""

    url = "https://amazon-product-reviews-keywords.p.rapidapi.com/product/search"

    querystring = {f"keyword": {amazonkeyword},
                   "country": {country}, "category": "aps"}

    headers = {
        'x-rapidapi-key': os.environ.get('AMAZON_REQUEST_KEY', key),
        'x-rapidapi-host': "amazon-product-reviews-keywords.p.rapidapi.com"
    }

    response = requests.request(
        "GET", url, headers=headers, params=querystring)
    result = json.loads(response.text)

    return result['products']


##########


@app.route('/')
def home_page():
    """ render the basic homepage"""

    return render_template('home.html')


@app.route('/search')
def search_result():
    """redner search result"""
    try:
        productname = request.args["productname"]
        brand = request.args["brand"]
        version = request.args["version"]
        country = request.args["country"]
        searchterm = brand+productname+version
        result = request_amazon(searchterm, country)
        return render_template('search.html', result=result, len=len(result), country=country)
    except:
        return render_template('500.html')


##########User ####

@app.route('/login', methods=["GET", "POST"])
def login_page():
    """render login form"""
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.authenticate(username, password)

        if user:
            session["username"] = user.username  # keep logged in
            flash(f"welcome! Dear {username}!")
            return redirect(f"users/{username}")
        else:
            form.username.errors = ["Password/Username Wrong!!!"]
            return render_template("login.html", form=form)

    return render_template('login.html', form=form)


@app.route("/signup", methods=['GET', 'POST'])
def signup():
    """render signup form"""

    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        profile_img = form.profile_img.data

        user = User.register(username, password, profile_img)
        db.session.add(user)

        db.session.commit()
        session['username'] = user.username

        return redirect(f"/users/{username}")

    else:

        return render_template("signup.html", form=form)


@app.route("/logout")
def log_out():
    """clear session and redirect"""
    session.pop("username")
    flash("you log out!")
    return redirect("/login")


@app.route("/users/<username>")
def show_user(username):
    """user profile page"""

    if 'username' not in session or username != session['username']:
        flash("You must be logged in to view!")
        return redirect("/")

    else:

        user = User.query.filter_by(username=username).first_or_404()
        profile_img = user.profile_img
        lists = ShoppingList.query.filter_by(username=username)
        userfav = user.userfav
        return render_template("username.html", user=user, profile_img=profile_img, lists=lists, userfav=userfav)

# user-delete user


@app.route("/users/<username>/delete", methods=['POST'])
def delete_user(username):
    """delete user"""
    if 'username' not in session or username != session['username']:
        flash("You must be logged in to view!")
        return redirect("/")

    else:
        user = User.query.filter_by(username=username).first_or_404()
        db.session.delete(user)
        db.session.commit()
        session.pop('username')

        return redirect("/login")

# user-edit userprofile
# user-add favorite


# error handle
# when there is 404 when the api returning result is none
@app.errorhandler(404)
def page_not_found(e):
    """customize error page"""
    return render_template('404.html'), 404

# when there is internal server error


@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500


# seach by asin page

def product_by_asin(asin, country):
    """return product details by asin"""

    url = "https://amazon-product-reviews-keywords.p.rapidapi.com/product/details"
    querystring = {f"asin": {asin}, "country": {country}}

    headers = {
        'x-rapidapi-key': os.environ.get('AMAZON_REQUEST_KEY', key),
        'x-rapidapi-host': "amazon-product-reviews-keywords.p.rapidapi.com"
    }

    response = requests.request(
        "GET", url, headers=headers, params=querystring)

    result = json.loads(response.text)

    return result['product']


def by_asin(asin):
    """return product details by asin"""

    url = "https://amazon-product-reviews-keywords.p.rapidapi.com/product/details"
    querystring = {f"asin": {asin}}

    headers = {
        'x-rapidapi-key': os.environ.get('AMAZON_REQUEST_KEY', key),
        'x-rapidapi-host': "amazon-product-reviews-keywords.p.rapidapi.com"
    }

    response = requests.request(
        "GET", url, headers=headers, params=querystring)

    result = json.loads(response.text)

    return result['product']


@app.route("/asin", methods=['GET', 'POST'])
def search_by_asin():
    """search by asin"""
    form = AsinSearchForm()
    if form.validate_on_submit():
        try:
            asin_search_term = form.ASIN.data
            #country = form.country.data
            result = by_asin(asin_search_term)
            return render_template('asinresult.html', result=result)
        except:
            return render_template('500.html')

    return render_template("asin.html", form=form)

# search reviews by asin


def search_reviews(asin):
    """get reviews by asin"""

    url = "https://amazon-product-reviews-keywords.p.rapidapi.com/product/reviews"

    querystring = {f"asin": {asin}, "variants": "1", "top": "0"}

    headers = {
        'x-rapidapi-key': os.environ.get('AMAZON_REQUEST_KEY', key),
        'x-rapidapi-host': "amazon-product-reviews-keywords.p.rapidapi.com"
    }

    response = requests.request(
        "GET", url, headers=headers, params=querystring)

    result = json.loads(response.text)

    return result['reviews']


@app.route("/product")
def product_detail():
    """display detail of the product"""
    asin = request.args["r"]
    #country = request.args["c"]
    result = by_asin(asin)
    reviews = search_reviews(asin)
    return render_template('product.html', result=result, reviews=reviews)


@app.route("/reviews", methods=['GET', 'POST'])
def reviews_by_asin():
    """return reviews by asin"""
    form = ReviewsByAsinForm()

    if form.validate_on_submit():
        try:
            review_search_term = form.reviewsByAsin.data
            #country = form.country.data
            result = search_reviews(review_search_term)
            return render_template('reviewresult.html', result=result)
        except:
            return render_template('500.html')

    return render_template('reviews.html', form=form)


# user shopping list
@app.route("/users/<username>/shoppinglist/add", methods=["GET", "POST"])
def new_shopping_list(username):
    """show add-shopping-list-form and process it"""

    if 'username' not in session or username != session['username']:

        flash("You must be logged in to view!")
        return redirect("/")

    form = ShoppingListForm()

    if form.validate_on_submit():
        content = form.content.data
        shoppinglist = ShoppingList(
            content=content,
            done=False,
            username=username
        )
        db.session.add(shoppinglist)
        db.session.commit()

        return redirect(f"/users/{shoppinglist.username}/shoppinglist/add")

    else:
        lists = ShoppingList.query.filter_by(username=username)
        return render_template("shoppinglist.html", form=form, lists=lists)


@app.route("/shoppinglist/<int:shoppinglist_id>/delete", methods=["POST"])
def delete_shopping_list(shoppinglist_id):
    """delete shoppinglist by id """
    shoppinglist = ShoppingList.query.get(shoppinglist_id)
    db.session.delete(shoppinglist)
    db.session.commit()

    return redirect(f"/users/{shoppinglist.username}/shoppinglist/add")


@app.route("/shoppinglist/<int:shoppinglist_id>/done")
def done_shoppinglist(shoppinglist_id):
    """toggle shoppinglist done status"""
    shoppinglist = ShoppingList.query.get(shoppinglist_id)
    if not shoppinglist:
        return redirect("/")
    if shoppinglist.done:
        shoppinglist.done = False
    else:
        shoppinglist.done = True
    db.session.commit()
    return redirect(f"/users/{shoppinglist.username}/shoppinglist/add")


# fix favicon error
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


# add favorite asin
@app.route('/addfav/<asin>', methods=["POST"])
def add_fav(asin):
    """add fav to users"""

    username = session['username']
    newFav = UserFav(username=username, asin=asin, fav=True)
    db.session.add(newFav)
    db.session.commit()

    return redirect(f"/users/{username}")


# remove favorite asin, hate this item!

@app.route('/removefav/<asin>', methods=["POST"])
def remove_fav(asin):
    """remove fav to users"""
    username = session['username']
    hate = UserFav(username=username, asin=asin, fav=False)
    db.session.add(hate)
    db.session.commit()

    return redirect(f"/users/{username}")

from flask import Flask,render_template,request,jsonify,redirect,flash,session,send_from_directory
from flask_debugtoolbar import DebugToolbarExtension
from models import db,connect_db,User,ShoppingList,UserFav

import os
import json
import requests

from forms import LoginForm,RegisterForm,AsinSearchForm, ReviewsByAsinForm, ShoppingListForm

app= Flask(__name__)

#connect database
app.config['SQLALCHEMY_DATABASE_URI'] = "postgres:///truedeal"
# compress the warning
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#echo the sql command
app.config['SQLALCHEMY_ECHO'] = True
#CONFIG THE DEBUGTOOL
app.debug = True
app.config['SECRET_KEY'] = 'SOMETHINGYOUDONTKNOW'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['TEMPLATES_AUTO_RELOAD'] = True

toolbar = DebugToolbarExtension(app)

#connect the app, database
connect_db(app)
#create table
db.create_all()

##function to search 
def request_amazon(amazonkeyword,country):

    """this will return json for the product keyword"""

    url = "https://amazon-product-reviews-keywords.p.rapidapi.com/product/search"

    querystring = {f"keyword": {amazonkeyword},"country":{country},"category":"aps"}

    headers = {
    'x-rapidapi-key': "e6001d6072msh1f868436da26ed9p1ce5c5jsnb7b3847e24ce",
    'x-rapidapi-host': "amazon-product-reviews-keywords.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    result = json.loads(response.text)
   
    return result['products']





def request_target(targetkeyword):
    """this will return json for the product keyword"""

    """targetApi"""
    url = "https://target-com-store-product-reviews-locations-data.p.rapidapi.com/product/search"

    querystring = {f"store_id":"3991","keyword": {targetkeyword},"sponsored":"1","limit":"50","offset":"0"}

    headers = {
    'x-rapidapi-key': "e6001d6072msh1f868436da26ed9p1ce5c5jsnb7b3847e24ce",
    'x-rapidapi-host': "target-com-store-product-reviews-locations-data.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    result = response.text

    return result


def request_walmart(walmartkeyword):

    """get walmart json information"""

    url = "https://search-walmart.p.rapidapi.com/"
    
    querystring = {f"name":{walmartkeyword}}

    headers = {
    'x-rapidapi-key': "e6001d6072msh1f868436da26ed9p1ce5c5jsnb7b3847e24ce",
    'x-rapidapi-host': "search-walmart.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    result = response.text

    return result
    

##########




@app.route('/')
def home_page():
    """ render the basic homepage"""


    return render_template('home.html')





@app.route('/search')
def search_result():
    """redner search result"""
    productname = request.args["productname"]
    brand=request.args["brand"]
    version=request.args["version"]
    country = request.args["country"]
    searchterm = brand+productname+version
    result = request_amazon(searchterm,country)

    username = session['username']
    
  
    #walmartresult =request_walmart(searchterm)
    #targetresult=request_target(searchterm)
    return render_template('search.html',result=result, len=len(result),username=username)


##########User ####

@app.route('/login', methods=["GET","POST"])
def login_page():
    """render login form"""
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.authenticate(username,password)

        if user:
            session["username"] = user.username #keep logged in
            flash(f"welcome! Dear {username}!")
            return redirect(f"users/{username}")
        else:
            form.username.errors = ["Password/Username Wrong!!!"]
            return render_template("login.html",form=form)
        

    return render_template('login.html',form=form)





@app.route("/signup", methods=['GET','POST'])
def signup():
    """render signup form"""

    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        profile_img = form.profile_img.data

        user = User.register(username,password,profile_img)
        db.session.add(user)

        db.session.commit()
        session['username'] = user.username

        return redirect(f"/users/{username}")
    
    else:
        
        return render_template("signup.html",form=form)



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
        lists = ShoppingList.query.filter_by(username = username)
        return render_template("username.html",user=user, profile_img=profile_img, lists=lists)

## user-delete user
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

## user-edit userprofile
## user-add favorite


##error handle

@app.errorhandler(404)
def page_not_found(e):
    """customize error page"""
    return render_template('404.html'),404
    


### seach by asin page

def product_by_asin(asin,country):
    """return product details by asin"""

    url = "https://amazon-product-reviews-keywords.p.rapidapi.com/product/details"
    querystring = {f"asin":{asin},"country":{country}}
    
    headers = {
    'x-rapidapi-key': "e6001d6072msh1f868436da26ed9p1ce5c5jsnb7b3847e24ce",
    'x-rapidapi-host': "amazon-product-reviews-keywords.p.rapidapi.com"
    }
    
    response = requests.request("GET", url, headers=headers, params=querystring)

    result = json.loads(response.text)
    
    return result['product']


    



@app.route("/asin",methods=['GET','POST'])
def search_by_asin():
    """search by asin"""
    form = AsinSearchForm()
    if form.validate_on_submit():
        asin_search_term = form.ASIN.data
        country = form.country.data
        result = product_by_asin(asin_search_term,country)
        return render_template('asin.html',form=form,result=result)
    
    return render_template("asin.html",form=form)







### search reviews by asin

def search_reviews(asin,country):
    """get reviews by asin"""

    url = "https://amazon-product-reviews-keywords.p.rapidapi.com/product/reviews"
    
    querystring = {f"asin":{asin},"country":{country},"variants":"1","top":"0"}
    
    headers = {
    'x-rapidapi-key': "e6001d6072msh1f868436da26ed9p1ce5c5jsnb7b3847e24ce",
    'x-rapidapi-host': "amazon-product-reviews-keywords.p.rapidapi.com"
    }
    
    response = requests.request("GET", url, headers=headers, params=querystring)

    result= json.loads(response.text)

    return result['reviews']



@app.route("/reviews", methods=['GET','POST'])
def reviews_by_asin():
    """return reviews by asin"""
    form = ReviewsByAsinForm()

    if form.validate_on_submit():
        review_search_term = form.reviewsByAsin.data
        country = form.country.data
        result = search_reviews(review_search_term,country)
        return render_template('reviews.html',form=form, result=result)

    return render_template('reviews.html',form=form)



#### user shopping list 
@app.route("/users/<username>/shoppinglist/add", methods=["GET","POST"])
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
            done = False,
            username = username
        )
        db.session.add(shoppinglist)
        db.session.commit()

        return redirect(f"/users/{username}")

    else:
        lists = ShoppingList.query.filter_by(username = username)
        return render_template("shopping_list.html",form=form,lists=lists)


@app.route("/shoppinglist/<int:shoppinglist_id>/delete", methods=["POST"])
def delete_shopping_list(shoppinglist_id):
    """delete shoppinglist by id """
    shoppinglist = ShoppingList.query.get(shoppinglist_id)
    db.session.delete(shoppinglist)
    db.session.commit()

    return redirect(f"/users/{shoppinglist.username}")
        

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
    return redirect(f"/users/{shoppinglist.username}")



### fix favicon error
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')



#### add favorite asin 
@app.route('/addfav/<asin>', methods=["POST"])
def add_fav(asin):
    """add fav to users"""

    asin = request.args["asin"]
    username=session['username']
    newFav = UserFav(username,asin )
    db.session.add(newFav)
    db.session.commit()

    return redirect("/")




    




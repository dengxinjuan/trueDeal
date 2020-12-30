from flask import Flask,render_template,request,jsonify,redirect,flash,session
from flask_debugtoolbar import DebugToolbarExtension
from models import db,connect_db,User

import requests

from forms import SearchForm,LoginForm,RegisterForm

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


def request_amazon(amazonkeyword):

    """this will return json for the product keyword"""

    url = "https://amazon-product-reviews-keywords.p.rapidapi.com/product/search"

    querystring = {f"keyword": {amazonkeyword},"country":"US","category":"aps"}

    headers = {
    'x-rapidapi-key': "e6001d6072msh1f868436da26ed9p1ce5c5jsnb7b3847e24ce",
    'x-rapidapi-host': "amazon-product-reviews-keywords.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    result = response.text
    return result




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
    searchterm = brand+productname+version
    result = request_amazon(searchterm)
    walmartresult =request_walmart(searchterm)
    targetresult=request_target(searchterm)
    return render_template('search.html',result=result,walmartresult=walmartresult,targetresult=targetresult)


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
            session['username'] = user.username
            flash(f"welcome! Dear {username}!")
            return redirect("/secret")
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

        return redirect(f"/secret")
    
    else:
        
        return render_template("signup.html",form=form)



@app.route("/logout")
def log_out():
    """clear session and redirect"""
    session.pop("username")
    flash("you log out!")
    return redirect("/login")

@app.route("/secret")
def secret():
    return render_template("secret.html")


@app.route("/users/<username>")
def show_user(username):
    user = User.query.get(username)
    profile_img = user.profile_img
    return render_template("user.html",user=user, profile_img=profile_img)






@app.route("/upc")
def search_by_upc():
    """search by upc"""

    return render_template("upc.html")




 

##create own api to return json, but it doesnt work.

"""@app.route("/api/search",methods=['POST'])
def call_amazon():

    received = request.json
    form =SearchForm(data=received)
    #brand = request.form.get("brand")
    productname = request.form["productname"]
    #version = request.form.get("version")

    amzresult = request_amazon(productname)
    #walresult = request_walmart(productname)
    #targetresult =request_target(productname)
    
    return amzresult"""







   

        




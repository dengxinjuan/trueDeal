from flask import Flask,render_template,request,jsonify
from flask_debugtoolbar import DebugToolbarExtension
import requests

from forms import SearchForm

app= Flask(__name__)
toolbar = DebugToolbarExtension(app)



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

@app.route('/login')
def login_page():
    """render login form"""
    return render_template('login.html')


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



@app.route("/signup")
def signup():
    """render signup form"""

    return render_template("signup.html")


@app.route("/upc")
def search_by_upc():
    """search by upc"""

    return render_template("upc.html")








##create own api to return json, but it doesnt work.

@app.route("/api/search",methods=['POST'])
def call_amazon():

    received = request.json
    form =SearchForm(data=received)
    #brand = request.form.get("brand")
    productname = request.form["productname"]
    #version = request.form.get("version")

    amzresult = request_amazon(productname)
    #walresult = request_walmart(productname)
    #targetresult =request_target(productname)
    
    return amzresult







   

        




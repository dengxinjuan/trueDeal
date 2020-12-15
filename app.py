from flask import Flask,render_template,request
import requests

app= Flask(__name__)

import requests



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




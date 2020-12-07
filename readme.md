#AppleTrueDeal Project 


##Goal

###To refine the data resources and narrow down the scope, I decide only use apple products as this demo project.

- return apple product price/description from amazon and walmart.
- combine amazon review,walmart review and give the product review rating.


##User Persona
 
-  Basic everyday user who wants to know what price for product will qualify for true deal, otherwise it will be a fake promo.
All ages. 
- Location: US marketplace, amazon/walmart user.
- User need: get the lowest price.

## API
- amazon price/description:

https://english.api.rakuten.net/ebappa1971/api/amazon-price/endpoints

https://rapidapi.com/axesso/api/axesso-amazon-data-service1

https://rapidapi.com/axesso/api/axesso-amazon-data-service1?endpoint=5c420736e4b0cc6cdc0edc7f

https://rapidapi.com/logicbuilder/api/amazon-product-reviews-keywords


- walmart price/description:
 https://developer.walmartlabs.com/docs?ref=apilist.fun

##Schema Design

- amazon: id-a, name, price, review, description
- walmart: id-w,name,price,review,description

- user login : id-user, username,password,profile-photo


- relation table 1:
user-amazon-favorite

- relation-table 2:
user-walmart-favorite

![schema image here](./truedeal.png)

##Simple Mockup
- search bar will include: 
Apple
Product category: 
product version:
other(optional)



![mockup image here](./mockup1.png)

![mockup image here](./mockup2.png)

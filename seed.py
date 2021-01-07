from models import db, User, ShoppingList
from app import app

db.drop_all()
db.create_all()

#add Users

cat = User(username="cat",password='cat',profile_img="https://pi.tedcdn.com/r/talkstar-assets.s3.amazonaws.com/production/playlists/playlist_325/talks_for_cat_lovers_1200x627.jpg?quality=89&w=800")


db.session.add(cat)
db.session.commit()

##add user shoppinglists
cat_list1 = ShoppingList(content="cat food",done= False,username="cat")
cat_list2 = ShoppingList(content="water",done= False,username="cat")
cat_list3 = ShoppingList(content="cat toy",done= True,username="cat")

db.session.add(cat_list1)
db.session.add(cat_list2)
db.session.add(cat_list3)

db.session.commit()

#### I dont know why my seed.py doesnt work?


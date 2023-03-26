# SP assignment 3
This is assignment 3 from structured programming created by Rico Megens.
In this project you will find three python files. 

# Querie runner
"querie_runner.py" is a python file for connection to a remote database and  for executing SQL queries and fetching data.

# Product recommendations
"products.py" is a python file for creating recommendations based on a random product id if none is given. It takes the
preference number of the product (which can be based of 'brand', 'gender', 'category', 'sub_category', 
'sub_sub_category', 'sub_sub_sub_category'). Next it takes products with the same preference number and returns them.

# Profile recommendation
"profile.py" is  file in which recommendations are done according to a profile. Similar products get recommended, viewed
before products get recommended again, similar products to viewed before get recommended, products similar to ordered, 
long viewings on products get recommended again and events in which products were clicked on, similar products get 
recommended. If the profile is new and has none of this (so lets say no events or products related to the profile) they get recommended random products which 
are recommendable and are frequently bought again.
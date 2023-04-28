from flask import Flask, render_template, request, flash

import psycopg2

from search import searchArgs
from restaurant import restaurant
from menu import menu, menus

conn = psycopg2.connect(database="rest", user="postgres", password="2104", host="localhost", port="5432")
print("Opened database successfully")


app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
      if request.method == 'POST':
         if request.form['username'] != 'admin' or request.form['password'] != 'admin':
               flash('Invalid credentials')
         else:
               flash('You were successfully logged in')
      return render_template('index.html')

@app.route('/update')
def update():
      return render_template('update.html')


@app.route('/search', methods=['GET'])
def search_restaurant():
   pincode = request.args.get('pincode')
   cuisine = request.args.get('cuisine')
   price = request.args.get('price')
   # create an instance of searchArgs
   args = searchArgs(cuisine, price, pincode)
   # execute the search
   restaurants = restaurant.search_restaurant(conn, args)

   return render_template('search.html', restaurants=restaurants)

@app.route('/showMenu', methods=['GET'])
def showMenu():
   # restaurant name will be button value
   restaurant_name = request.args.get('name')
   rest_id = request.args.get('id')
   # execute the search
   menus_list = menu.search_menu(conn, restaurant_name, rest_id)
   # create an instance of menus
   menus_arg = menus(restaurant_name, rest_id, menus_list)

   return render_template('menu.html', menus=menus_arg)

   





if __name__ == '__main__':
   # run on port 5006
   app.run(debug=True, port=5006)
from flask import Flask, render_template, request, flash, redirect, url_for, session

import psycopg2
import uuid

from search import searchArgs
from restaurant import restaurant
from menu import menu, menus

conn = psycopg2.connect(database="rest", user="postgres", password="2104", host="localhost", port="5432")


app = Flask(__name__)

app.secret_key = 'super secret key'


@app.route('/')
def index():
   if 'username' in session:
      pincode = request.args.get('pincode')
      cuisine = request.args.get('cuisine')
      price = request.args.get('price')
      dish = request.args.get('dish')
      # create an instance of searchArgs
      args = searchArgs(cuisine, price, pincode, dish)
      # execute the search
      restaurants = restaurant.search_restaurant(conn, args)
      return render_template('index.html', restaurants=restaurants)
   else:
      return redirect(url_for('login'))

@app.route('/login', methods=['POST', 'GET'])
def login():
   if 'session_token' in session:
      return redirect(url_for('index'))
   if request.method == 'POST':
      username = request.form['email']
      password = request.form['userPassword']
      print (username, password)
      if username == 'admin' and password == 'admin':
         session['username'] = username
         session['session_token'] = str(uuid.uuid4())
         return redirect(url_for('index'))
      else:
         return  render_template('login.html', error='Invalid username or password')
   return render_template('login.html')

@app.route('/signup', methods=['POST', 'GET'])
def signup():
   return render_template('signup.html')


@app.route('/update')
def update():
   return render_template('update.html')


@app.route('/search', methods=['GET'])
def search_restaurant():
   pincode = request.args.get('pincode')
   cuisine = request.args.get('cuisine')
   price = request.args.get('price')
   dish = request.args.get('dish')
   # create an instance of searchArgs
   args = searchArgs(cuisine, price, pincode, dish)
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

   
@app.route('/logout')
def logout():
   session.pop('username', None)
   session.pop('session_token', None)
   return redirect(url_for('login'))




if __name__ == '__main__':
   # run on port 5006
   app.run(debug=True, port=5006)
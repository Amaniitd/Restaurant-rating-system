from flask import Flask, render_template, request, flash, redirect, url_for, session

import psycopg2
import uuid

from search import searchArgs
from restaurant import restaurant
from menu import menu, menus

conn = psycopg2.connect(database="rest", user="postgres", password="2104", host="localhost", port="5432")


app = Flask(__name__)

app.secret_key = 'super secret key'


def isUserExists(email, password):
   # create a cursor
   cur = conn.cursor()
   # execute a query
   exe_cmd = "SELECT * FROM users WHERE email = '" + email + "' AND password = '" + password + "';"
   print (exe_cmd)
   cur.execute(exe_cmd)
   # fetch the results
   rows = cur.fetchall()
   # close the cursor
   cur.close()
   if len(rows) == 0:
      return False
   else:
      return True

def getUserId (email, password):
   # create a cursor
   cur = conn.cursor()
   # execute a query
   exe_cmd = "SELECT id FROM users WHERE email = '" + email + "' AND password = '" + password + "';"
   print (exe_cmd)
   cur.execute(exe_cmd)
   # fetch the results
   rows = cur.fetchall()
   # close the cursor
   cur.close()
   if len(rows) == 0:
      return -1
   else:
      return rows[0][0]


def createUser(name, email, password):
   if isUserExists(email, password):
      return -1
   else:
      # max of all existing user ids
      cur = conn.cursor()
      exe_cmd = "SELECT MAX(id) FROM users;"
      cur.execute(exe_cmd)
      rows = cur.fetchall()
      cur.close()
      max_id = rows[0][0]
      if max_id == None:
         max_id = 1
      # create a cursor
      cur = conn.cursor()
      # execute a query
      exe_cmd = "INSERT INTO users VALUES (" + str(max_id + 1) + ", '" + name + "', '" + email + "', '" + password + "');"
      print (exe_cmd)
      cur.execute(exe_cmd)
      # commit the changes
      conn.commit()
      # close the cursor
      cur.close()
      return max_id + 1



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
      userEmail = getEmail(session['username'])
      return render_template('index.html', restaurants=restaurants, userEmail=userEmail)
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
      if isUserExists(username, password):
         session['username'] = getUserId(username, password)
         session['session_token'] = str(uuid.uuid4())
         return redirect(url_for('index'))
      else:
         return  render_template('login.html', error='Invalid username or password')
   return render_template('login.html')

@app.route('/signup', methods=['POST', 'GET'])
def signup():
   if 'session_token' in session:
      return redirect(url_for('index'))
   if request.method == 'POST':
      name = request.form['name']
      email = request.form['email']
      password = request.form['userPassword']
      print (name, email, password)
      user_id = createUser(name, email, password)
      if user_id != -1:
         session['username'] = user_id
         session['session_token'] = str(uuid.uuid4())
         return redirect(url_for('index'))
      else:
         print ("User already exists")
         return  render_template('signup.html', error='User already exists')
   return render_template('signup.html')


@app.route('/update')
def update():
   return render_template('update.html')


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


def isRated(user_id, restaurant_id):
   # create a cursor
   cur = conn.cursor()
   # execute a query
   exe_cmd = "SELECT * FROM Rating WHERE user_id = '" + str(user_id) + "' AND restaurant_id = '" + str(restaurant_id) + "';"
   print (exe_cmd)
   cur.execute(exe_cmd)
   # fetch the results
   rows = cur.fetchall()
   # close the cursor
   cur.close()
   if len(rows) == 0:
      return False
   else:
      return True

def getEmail(userid):
   # create a cursor
   cur = conn.cursor()
   # execute a query
   exe_cmd = "SELECT email FROM users WHERE id = '" + str(userid) + "';"
   print (exe_cmd)
   cur.execute(exe_cmd)
   # fetch the results
   rows = cur.fetchall()
   # close the cursor
   cur.close()
   if len(rows) == 0:
      return ""
   else:
      return rows[0][0]

def updateRating(restaurant_id, overall, food, service, ambience):
   # create a cursor
   cur = conn.cursor()
   # max of all existing ids
   exe_cmd = "SELECT MAX(id) FROM Rating;"
   cur.execute(exe_cmd)
   rows = cur.fetchall()
   cur.close()
   max_id = rows[0][0]
   if max_id == None:
      max_id = 1
   
   user_id = session['username']
   
   # id, user_id, restaurant_id, overall, food, service, ambience

   # if user has already rated the restaurant, update the rating
   exe_cmd = ""
   if isRated(user_id, restaurant_id):
      exe_cmd = "UPDATE Rating SET total_rating = " + str(overall) + ", food_rating = " + str(food) + ", service_rating = " + str(service) + ", ambience_rating = " + str(ambience) + " WHERE user_id = " + str(user_id) + " AND restaurant_id = " + str(restaurant_id) + ";"
   else:
      exe_cmd = "INSERT INTO Rating VALUES (" + str(max_id + 1) + ", '" + str(user_id) + "', '" + str(restaurant_id) + "', '" + str(overall) + "', '" + str(food) + "', '" + str(service) + "', '" + str(ambience) + "');"

   # create a cursor
   cur = conn.cursor()


   cur.execute(exe_cmd)
   # commit the changes
   conn.commit()
   # close the cursor
   cur.close()

@app.route('/rating' , methods=['POST'])
def rating():
   overall = request.form['overall_rating']
   food = request.form['food_rating']
   service = request.form['service_rating']
   ambience = request.form['ambience_rating']
   id = request.form['id']
   updateRating(id, overall, food, service, ambience)
   return render_template('rating.html')



@app.route('/rate', methods=['POST'])
def rate():
   restaurant_id = request.form['id']
   return render_template('rate.html', id = restaurant_id)


if __name__ == '__main__':
   # run on port 5006
   app.run(debug=True, port=5006)
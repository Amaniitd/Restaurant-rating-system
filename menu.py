

class menu:
   def __init__(self, name, price, category, description):
      self.name = name
      self.price = price
      self.category = category
      self.description = description

   def search_menu(conn, rest_id):
      # create a cursor
      cur = conn.cursor()
      # execute a query
      cur.execute("SELECT * FROM Dish WHERE restaurant_id = %s", (rest_id,))
      # fetch the results
      rows = cur.fetchall()
      # close the cursor
      cur.close()
      # create a list to hold the restaurant objects
      menus = []
      # iterate through the result set and create restaurant objects
      for row in rows:
         menus.append(menu(row[2], row[4], row[1], row[3]))
      # return the list
      return menus

class menus:
   def __init__(self, restaurant_name, id, menus):
      self.restaurant_name = restaurant_name
      self.id = id
      self.menus = menus
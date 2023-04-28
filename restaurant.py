
class restaurant:
   def __init__(self, id, name, address, priceRange, zipcode):
      self.id = id
      self.name = name
      self.address = address
      self.priceRange = priceRange
      self.zipcode = zipcode

   # execute the search in the database
   
   def search_restaurant(conn, args):
      # create a cursor
      cur = conn.cursor()
      # execute a query
      cur.execute("SELECT * FROM restaurant LIMIT 3")
      # fetch the results
      rows = cur.fetchall()
      # close the cursor
      cur.close()
      # create a list to hold the restaurant objects
      restaurants = []
      # iterate through the result set and create restaurant objects
      for row in rows:
         restaurants.append(restaurant(row[0], row[1], row[2], row[3], row[4]))
      # return the list
      return restaurants
   
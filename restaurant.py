
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
      where_clause = "WHERE "
      if args.cuisine:
         where_clause += "id IN (SELECT restaurant_id FROM Cuisines WHERE cuisine_type = '" + args.cuisine + "') AND "
      if args.price:
         p = "$$$$"
         if args.price == "1":
            p = "$"
         elif args.price == "2":
            p = "$$"
         elif args.price == "3":
            p = "$$$"
            
         where_clause += "priceRange = '" + p + "' AND "
      if args.zipcode:
         where_clause += "zipcode = '" + args.zipcode + "' AND "
      if args.dish:
         where_clause += "id IN (SELECT restaurant_id FROM Dish WHERE name = '" + args.dish + "') AND "
      
      if where_clause == "WHERE ":
         where_clause = ""
      else:
         where_clause = where_clause[:-5]
      print (where_clause)
      exe_cmd = "SELECT * FROM restaurant " + where_clause + " limit 100;"
      print (exe_cmd)
      cur.execute(exe_cmd)
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
   
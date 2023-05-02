
class restaurant:
   def __init__(self, id, name, address, priceRange, zipcode, rate_count, avg_rating):
      self.id = id
      self.name = name
      self.address = address
      self.priceRange = priceRange
      self.zipcode = zipcode
      self.rate_count = rate_count
      self.avg_rating = avg_rating

   # execute the search in the database
   
   def search_restaurant(conn, args):
      # create a cursor
      cur = conn.cursor()
      # execute a query
      where_clause = "WHERE "
      if args.cuisine:
         where_clause += "id IN (SELECT restaurant_id FROM Cuisines WHERE cuisine_type = '" + args.cuisine + "') AND "
      if args.price and args.price != "0":
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
      exe_cmd1 = "SELECT * FROM restaurant " + where_clause + " limit 100"
      
      exe_cmd = "with t1 as (" + exe_cmd1 + ") select t1.id, name, fullAddress, priceRange, zipCode, count(*) as rate_count, cast(COALESCE(avg(total_rating), 0)as DECIMAL(10, 1)) as avg_rating from t1 left join Rating on t1.id = Rating.restaurant_id group by t1.id, name, fullAddress, priceRange, zipCode order by avg_rating desc, rate_count desc limit 100;"
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
         restaurants.append(restaurant(row[0], row[1], row[2], row[3], row[4], row[5], row[6]))
      # return the list
      return restaurants

   def get_owner_restaurants(conn, userid):
      # create a cursor
      cur = conn.cursor()
      # execute a query
      exe_cmd = "SELECT restaurant_id FROM Owner WHERE user_id = " + str(userid) + ";"
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
         # create a cursor
         cur = conn.cursor()
         # execute a query
         exe_cmd = "with t1 as (SELECT * FROM restaurant WHERE id = " + str(row[0]) + ") select t1.id, name, fullAddress, priceRange, zipCode, sum(case when total_rating IS NOT NULL then 1 else 0 end) as rate_count, cast(COALESCE(avg(total_rating), 0)as DECIMAL(10, 1)) as avg_rating from t1 left join Rating on t1.id = Rating.restaurant_id group by t1.id, name, fullAddress, priceRange, zipCode;"
         print (exe_cmd)
         cur.execute(exe_cmd)
         # fetch the results
         rows1 = cur.fetchall()
         # close the cursor
         cur.close()
         # iterate through the result set and create restaurant objects
         for row1 in rows1:
            restaurants.append(restaurant(row1[0], row1[1], row1[2], row1[3], row1[4], row1[5], row1[6]))
      # return the list
      return restaurants

   
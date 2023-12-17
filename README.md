# Messaging System 

#App 1 

We have producer.py,  which takes any json file as input and sent RabbitMQ queue

#App 2

We have a consumer.py , which takes the data from the quue and transports data to postgress DB.

#App 3 

We have multiple api endpoints in Flask : 

1. /view - simple UI to view all the information like all avaialble product jsons ,  can also filter on instock products , has a search bar to search products based on sku.
2. /availability-score - shows availability score , total instock product count , total product count
3. /products - displays all products

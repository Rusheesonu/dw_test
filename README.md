# Messaging System 

#App 1 

We have producer.py,  which takes any json file as input and sent RabbitMQ queue

#App 2

We have a consumer.py , which takes the data from the quue and transports data to postgress DB.

ANd the Db schema and details are provided in test_db.sql

#App 3 

We have multiple api endpoints in Flask : 

1. /view - simple UI to view all the information like all avaialble product jsons ,  can also filter on instock products , has a search bar to search products based on sku.
2. /availability-score - shows availability score , total instock product count , total product count
3. /products - displays all products


Entire soulution is Dockerized

To Run the Project : 

- git clone
- cd project folder
-- docker-compose up --build

-
-
-
-
- <img width="1559" alt="Screenshot 2023-12-17 at 16 13 25" src="https://github.com/Rusheesonu/dw_test/assets/23713918/5aa0605b-f582-4e2a-85fd-7a08c90c2a8e">



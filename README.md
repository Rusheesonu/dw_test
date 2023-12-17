# Messaging System 

#App 1 

We have producer.py, which takes any json file as input and sends the data RabbitMQ queue

#App 2

We have a consumer.py, which takes the data from the RabbitMQ queue and transports the data to postgress DB.

And the Db schema and details are provided in test_db.sql

#App 3 

We have multiple api endpoints in Flask : 

1. /view - simple UI built to view all the information like all avaialble product jsons ,  can also filter on instock products , has a search bar to search products based on sku.
2. /availability-score - shows availability score , total instock product count , total product count
3. /products - displays all products


Entire soulution is Dockerized.

To Run the Project : 

- git clone
- cd project folder
- docker-compose up --build

# Availability Score Endpoint
  
  <img width="1559" alt="Screenshot 2023-12-17 at 16 13 25" src="https://github.com/Rusheesonu/dw_test/assets/23713918/5aa0605b-f582-4e2a-85fd-7a08c90c2a8e">


# All Products View 

  <img width="1557" alt="Screenshot 2023-12-17 at 15 50 07" src="https://github.com/Rusheesonu/dw_test/assets/23713918/02378ea1-8b3e-4c54-a425-d9ee0110ab58">

# Sku Search View 

  <img width="1561" alt="Screenshot 2023-12-17 at 16 11 28" src="https://github.com/Rusheesonu/dw_test/assets/23713918/2ab6fba9-11b7-4f79-b157-3bebf12b143e">

# All Products Endpoint

  <img width="1562" alt="Screenshot 2023-12-17 at 16 13 37" src="https://github.com/Rusheesonu/dw_test/assets/23713918/44306c50-c146-4b9a-a4d2-6d0c3bf34f38">

  


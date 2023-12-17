-- Create Product table
CREATE TABLE Product (
    product_id SERIAL PRIMARY KEY,
    reference_product_id VARCHAR(255),
    source VARCHAR(50),
    store_code VARCHAR(50)
);

-- Create Location table
CREATE TABLE Location (
    location_id SERIAL PRIMARY KEY,
    postal_zip_code VARCHAR(20),
    postal_zip_name VARCHAR(100),
    place_name VARCHAR(100),
    admin_name1 VARCHAR(100)
);

-- Create PriceInfo table
CREATE TABLE PriceInfo (
    price_id SERIAL PRIMARY KEY,
    product_id INTEGER REFERENCES Product(product_id),
    location_id INTEGER REFERENCES Location(location_id),
    available_price DECIMAL,
    stock VARCHAR(20),
    crawl_page_counter INTEGER,
    major_version_end_time TIMESTAMP,
    bundle_match_type VARCHAR(50),
    bundle_definition_hash VARCHAR(255)
);



'''
Tables:

Product:

Columns:

product_id (Primary Key)
reference_product_id
source
store_code
Location:

Columns:

location_id (Primary Key)
postal_zip_code
postal_zip_name
place_name
admin_name1
PriceInfo:

Columns:

price_id (Primary Key)
product_id (Foreign Key referencing Product table)
location_id (Foreign Key referencing Location table)
available_price
stock
crawl_page_counter
major_version_end_time
bundle_match_type
bundle_definition_hash


Product table: Stores information about the products, their identifiers, sources, and store codes.
Location table: Contains details about the location such as postal information and place details.
PriceInfo table: Holds the specific price information along with other metadata related to products at certain locations.

By normalizing the data into different tables based on their distinct entities, it follows the principles of database normalization. 

Benefits of the Chosen Structure:

Data Consistency:

By breaking down the data into separate tables, it becomes easier to maintain data consistency. For instance, if a location\'s details change, it only needs to be updated in the Location table, and the changes will reflect across all related records in the database.

Scalability:

The chosen structure allows for easy scalability. New products, locations, or price information can be added without altering the existing schema significantly. This scalability is crucial for accommodating future data expansion.

Query Optimization:

The use of foreign keys facilitates efficient querying by allowing joins between tables. For example, fetching price information for a specific product in a particular location can be done by joining the Product, Location, and PriceInfo tables based on their respective keys.

Data Integrity:

The schema design supports data integrity by utilizing primary and foreign keys. This ensures that each record is uniquely identified and maintains referential integrity between tables, preventing or minimizing data inconsistencies.

'''

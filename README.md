### API for technical test for CircularX

## How to launch

Due to problem of networks between two containers. It need some operation :
- Launch "docker-compose up" to launch a docker PostGreSQL with the correct table
    - If you want use your personnel PostGreSQL, you could setup three environement variable to connect to other instance "USERNAME_DB", "PASSWORD_DB" and "DATABASE". The SQL script to create table and triggers is available in SQL folder
- Launch "init_table.py" if you want to add the data.csv to SQL
- Launch "api.py" to launch the API to manage SQL instance

## SQL

# Products

Table of products which contains :
- id
- name of product
- average of price, auto compute by trigger on table of sells

# Sells

Table of sells which contains :
- id
- name of shop
- product id, foreign key which reference to id of product table
- date of sell
- price

Line of sell is delete in cascade when a product is delete

## Python

# init_table.py

This script permit to initialize table with data.csv file

# API

The API is launch by app.py

It contains two resources "products" and "sells".

Only route GET has accessible without Authentication. The other route need an authentication by Basic Authentication with the credentials admin/admin : -H "Authorization: Basic YWRtaW46YWRtaW4="

*products*
- The creation (POST) of product need only the field "name"
- The update (PUT) could only update the field "name"
- The delete (DELETE) delete the product and all linked sells
- The get (GET) permit to get one product /products/{id} or /products. The /products list by default the ten first items, the query "limit" and "offset" could be used for get other products


*sells*
- The creation (POST) of product need field :
    - shop
    - sell_date
    - price
    - product_id or product_name
- The update (PUT) could update all field but not works by product_name
- The delete (DELETE) delete the sells
- The get (GET) permit to get one sell /sells/{id} or /sells. The /sells list by default the ten first items, the query "limit" and "offset" could be used for get other sells
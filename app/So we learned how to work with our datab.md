So we learned how to work with our databse by using Postgres SQL language but now we want to connect  python to our PostgreSQL databases. So to connect it we will use "Psycopg" to execute SQL queries , manage database connections, handle transactions , and retrieve data from PostgreSQL databases using Python code:

to work with Pyscopg we installed psycopg  and psycopg2 via pip

traditional way of interacting with our postgres driver is by sending sql commands as we have seen 

so if we use ORM instead of directly interacting with the postgres database by usign sql command we can use ORM(object relational mapper) that could function as intermediary between FASTAPI AND POSTGRES DATABASE and using such intermediary could enable us to use more common python statements

we  use SQLALCHEMY as ORM to connect to database:

steps:
pip install sqlalchemy 
we also have to have psycopg2 installed in our environment

we created a file called database.py

and then we created a file called model.py within our app folder again
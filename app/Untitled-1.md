#If we want to document our code we can simply type in google   http://127.0.0.1:8000/docs    which will show us documentation of our code and any time we modify our code it will update it instantly

POSTGRESQL for database management(here you can study for retrivig queries on sql:   https://www.postgresqltutorial.com/):

so we created our local host server, then upon this we created our FASTAPI database(but we can name the database anything we want), then upon it we created a table where put some variables and entered some corresponding values, then we are quering for our table: 

if we type in our query : SELECT * FROM products;       this will give us all the columns from our table named products , if we wanna get only some specific columns which are variables in fact we can specify their name instead of * which calls all the columns. so        SELECT NAME FROM products;  will only call the NAME column in the producgs table

if we want to rename our column variable we can use this SQL statement: SELECT id AS products_id, is_sale AS on_sale FROM products;
so this would rename id as products_id and is_sale as on_sale

if want to call the data row based on certain id:    SELECT * FROM products WHERE id = 10;   this will show the data entry with id 10
if we want to call data with inventory 0 :  SELECT * FROM products WHERE inventory = 0;  
for string characters we have to put 'name'  like:   SELECT * FROM products WHERE name = 'TV';
 
 if we want specify some variables to be equal to some values instead of using or we can shortly write as: SELECT * FROM products WHERE id IN (1,2,3);  

 if we wanna call any value that starts with smt but does not matter how it goes:  SELECT * FROM products WHERE name LIKE 'TV%';   So this statement would call all the values in the name variable that starts with TV

 SELECT * FROM products ORDER BY price;  this statement will order a variable price in this case in ascendign order so we use ORDER BY

 to get limited number of output :   SELECT * FROM products LIMIT 10;

 to insret data to database we can use:   INSERT INTO products (name, price, inventory) VALUES ('tortilla',4,1000); 
 if we said :  INSERT INTO products (name, price, inventory) VALUES ('tortilla',4,1000) returning *;    this would return all the columns after an entry is created

 to delete data from database:   DELETE FROM products WHERE id = 10;

 to update a product:    UPDATE products SET name = 'flour tortilla ', price = 40 WHERE id = 25;

 JOINING 2 TABLES ON POSTGRES:
 SELECT * FROM posts LEFT JOIN users ON posts.owner_id = users.id;  So this line of code will go to users table and find the rows that have the same id with the owner_id that represent the owners of the post and then it will merge it with the table of Posts
 #just make sure that if the users and posts table have the columns named same you have to then indicate columns such as posts.id and 
 users.id 

RIGHT JOIN will show things that exist on the RIGHT table but does not neccessarily exist on the left table
LEFT JOIN will show things that exist on the LEFT table but does not neccessarily exist on the RIGHT table

SELECT users.id,users.email, COUNT(posts.id)as user_post_count FROM posts RIGHT JOIN users ON posts.owner_id = users.id group by users.id;   #here we select the columns we wanna output so in this case from users table id and email we want them to get displayed, and we are counting the number of posts created by each user by using the conditionality of posts.owner_id = users.id 

SELECT posts.*,COUNT(votes.post_id) as votes from posts LEFT JOIN votes ON posts.id = votes.post_id group by posts.id;   #this is for counting the number of votes on posts in total




  
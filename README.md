# back-Attendance

---

## Using Database MySQL

Go to '.../app/main/' path and open 'config.py' file

**Modify A code to B code**

### `A code`

    ...
    
    db = {
	    'user' : 'admin',
	    'password' : '1234',
	    'host' : 'localhost',
	    'port' : 3306,
	    'database' : 'User_DB'
    }
    
    ...
    
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://admin:1234@localhost:3306/User_DB?charset=utf8".format()

 

### `B code`

    db = {
	    'user' : 'your_User', # create MySQL your user
	    'password' : 'your_User_password', # create MySQL your User Password
	    'host' : 'localhost', # Using Local Server
	    'port' : 3306, # Using Local Port
	    'database' : 'your_DB' # Using your MySQL Database
    }
    
    ...
    
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://**your_User**:**your_User_password**@localhost:3306/**your_DB**?charset=utf8".format()

---

## Start Server Using Flask

    pip install -r requirements.txt
    
    python manage.py run

---

## Start Database

    python manage.py db init
    
    python manage.py db migrate
    
    python manage.py db upgrade

---

# Base Server Code

---

# Reference git hub url

https://github.com/cosmic-byte/flask-restplus-boilerplate/tree/master

---

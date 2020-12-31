![image](sose.png)
***
The Simple Online Store Engine based on the [Flask](https://flask.palletsprojects.com/) framework.  
SOSE - the responsive web app, under the hood also: [Bootstrap framework](https://getbootstrap.com),
[Bootstrap table](https://bootstrap-table.com), [Bootstrap icons](https://icons.getbootstrap.com),
[Font Awesome](https://fontawesome.com/), [jQuery](https://jquery.com/), [Axios](https://github.com/axios/axios)

This project is the result of the [final assignment](https://cs50.harvard.edu/x/2020/project/) of the
Harvard [CS50 course](https://cs50.harvard.edu/x/2020/) project.

## Install

***

Clone the git repository

```
$ git clone https://github.com/dudilona/sose
$ cd sose
```

Create a virtualenv and activate it:

```
$ python3 -m venv venv
$ . venv/bin/activate
```

Or on Windows cmd:

```
> py -3 -m venv venv
> venv\Scripts\activate.bat
```

Install SOSE:

```
$ pip install -e .
```

## Run

***

```
$ export FLASK_APP=src
$ export FLASK_ENV=development
$ flask init-db
$ flask run
```

Or on Windows cmd:

```
> set FLASK_APP=src
> set FLASK_ENV=development
> flask init-db
> flask run
```

Open http://127.0.0.1:5000 in a browser.

## Usage

***

- Click the registration link and register a new user  
  Note - the first registered user **becomes an administrator**  
  Now you have access to the admin panel
- Go to the admin panel, and you will see 4 section: settings, users, products, orders
- In the global section you can change main content of the site:
  - Global: Store name (title)
  - Global: Site icon - favicon.ico
  - Global: Footer description
  - Main page header
  - Main page image
  - Main page description
  - Contacts: Phone number
  - Contacts: Email
  - Contacts: Address
  - Contacts: Google map
- In the users section you can manage the users table:
  - Searching users
  - Sorting users
  - Edit / Delete users
  - Make users administrators
  - Change users passwords
- In the products section you can manage the products table:
  - Add new products
  - Searching products
  - Sorting products
  - Edit / Delete products
- In the orders section you can see the history of orders:
  - Searching orders
  - Sorting orders
- After adding products in the admin panel, you can go to the catalog and check that the products exist
- You can open the products and buy them (move to cart)
- You can open the cart and:
  - Searching product items in the cart
  - Sorting product items in the cart
  - Delete product items from the cart
  - Make the order
  - You can make order in 2 modes: authorized and unauthorized 
- In the contacts page you can see the contacts and google map
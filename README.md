# Please Money

## overview of the system

## version
- python 3.6.4 or greater
- postgres 11.5 or greater
- psycopg2 2.8.4
- selenium 3.141.0
- beautifulsoup4 4.6.0
- chrome-version 78

## directory tree
```
.
├── README.md
├── app.yaml
├── flaskapp
│   ├── app.py
│   ├── chromedriver
│   │   └── 78
│   │       └── chromedriver.exe
│   ├── json
│   │   └── line.json
│   ├── lib
│   │   ├── __pycache__
│   │   ├── push_line.py
│   │   └── utils.py
│   ├── scraping_schedule.py
│   ├── static
│   │   └── style.css
│   └── templates
│       ├── base.html
│       └── index.html
└── scraping
    ├── __init__.py
    ├── __pycache__
    ├── chromedriver
    │   └── 78
    │       └── chromedriver.exe
    ├── json
    │   └── login_info.json
    ├── lib
    │   ├── extract_content.py
    │   └── get_html.py
    ├── manage_db.py
    └── scraping_function.py
```

## setup
Install postgres from https://www.enterprisedb.com/downloads/postgres-postgresql-downloads
Set environment variables

### Create database
```
$ psgl -U postgres
(Input Password)

postgres=# create database please_money;
(dhisplay "CREATE DATABASE" if success)
postgres=# \q
```

## usage
### Management Table
```
$ cd please_money/scraping
$ python manage_db.py -f c  # create payment table and bank table 
$ python manage_db.py -f d -t payment # drop payment table
$ python manage_db.py -f i -t bank  # initializa bank table
```

### Run
```
$ cd please_money/flaskapp
$ python app.py
$ python scraping_schedule.py
```

### LINE notification
copy and paste "LINE access token" to 
```
please_money/flaskapp/json/line.json
```
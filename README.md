# Tweetie
## *Introduction*

### Summary

> - Project
>   - Fetch you Home Timeline Tweets from Twitter Account
>   - Twitter Social Login
>   - Able to analyze the tweets having links in the text area and user who share maximum number of tweets having links
>  </br>
>
> - BACKEND
>   - Using Flask for storing sessions and doing analysis part
>   - Authlib for Twitter oauth authorization
>  <br/>
>
> - FRONTEND
>   - Flask defaults Jinja2 Templating Engine
>   - Bootstrap, Jquery for some styling

### Requirements

> - BACKEND
>   - [Python 3.8.5](https://www.python.org/downloads/release/python-385/)
>   - [Flask 1.1.2](https://pypi.org/project/Flask/)
>   - [Authlib 0.14.3](https://authlib.org/)
>  <br/>
>
> - FRONTEND
>   - [JQuery](https://code.jquery.com/)
>   - [Bootstrap 4.5](https://getbootstrap.com/docs/4.5/getting-started/download/)
>  <br/>
>
> - Database
>   - [Heroky Postgre (for Deployment)](https://www.heroku.com/postgres)
>   - [SQLAlchemy (As ORM)](https://www.sqlalchemy.org/)

## Project Structure

```bash

.
├── static
│   └── imgs
│       ├── icon
│       └── twitter
├── templates
│   ├── about.html
│   ├── analyze.html
│   ├── base.html
│   ├── error.html
│   ├── index.html
│   └── tweets.html
├── app.py
├── config.py
├── Procfile
├── README.md
└── requirements.txt
```

## How to Reproduce


* **Step 1: Clone the Project**
```python3
git clone https://github.com/pawangeek/Tweetie
cd Tweetie
```
* **Step 2: Create a virtual environment**
```Python
# For mac and linux users
python3 -m venv env
source env/bin/activate

# For window users
py -m venv env
.\env\Scripts\activate
```
* **Step 3: Load all dependencies from requirements.txt**
```python
pip install -r requirement.txt
```
* **Step 4: Create a project at Heroku and link that in your local enviroment**
```
-> Go to https://dashboard.heroku.com/apps and create a new project
-> Login from remote by heroku login
-> COnnect remote to this app
```
* **Step 5: Create a postgres database from Heroku to deploy**
```python
Go to https://data.heroku.com/ select heroku postgres
Bind you recently create app and get the url for database
```
* **Step 6: Put the postgres database link into into app.config['SQLALCHEMY_DATABASE_URI'] in app**

* **Step 7: Open Python terminal and create database tables like this**
```python
from app import db 
db.create_all()
```

* **Step 8: Go to [twitter developer](https://developer.twitter.com/en) console**
```python
Add callback url : http://127.0.0.1:5000/auth
Another callback url http://[your-webapp]-herokuapp.com/auth
```
* **Step 9: Get the twitter_client_id and twitter_client_secret from that twitter dev console**
```python
# Add them here
TWITTER_CLIENT_ID = ''
TWITTER_CLIENT_SECRET = ''
```
* **Step 10 Now deploy it to heroku**
```python 
git init .
git commit -am "Make it awesome"
git origin heroku master
```

* **Step 11 Boom you will see you this app running on  website/ localhost.**

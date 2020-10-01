# Tweetie

* Step 1 Create a virtual environment
* Step 2 Load all dependencies from requirements.txt
* Step 3 Create a project at Heroku and link that in your local enviroment
* Step 3 Create a postgres database from Heroku to deploy
* Step 4 Put the postgres database link into into app.config['SQLALCHEMY_DATABASE_URI'] in app
* Step 5 Open Python terminal and write `from app import db` followed by `db.create_all()`
* Step 6 Initialize a git repo by `git init .`
* Step 7 GO to twitter developer console and add any app name and callback url : `http://127.0.0.1:5000/auth` and the one on which we are going to host `http://myweb-herokuapp.com/auth`
* Step 8 Get the twitter_client_id and twitter_client_secret from that app and add them into the config.py
* Step 9 Now add everything to heroku by `git commit -am "Make it awesome"`
* Step 10 And Finally `git origin heroku master` to launch website
* Step 11 Now over your website/ localhost. You will get all further endpoints instructions at /about

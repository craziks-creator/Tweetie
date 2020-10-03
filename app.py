from flask import Flask, url_for, request
from flask import session, render_template, redirect
from authlib.integrations.flask_client import OAuth, OAuthError
from datetime import datetime, timedelta
import re, json, requests
from urllib.parse import urlparse
from urllib.request import urlopen
from flask_sqlalchemy import SQLAlchemy


sevendays = datetime.today() - timedelta(days=7)
app = Flask(__name__)

app.secret_key = '!secret'
app.config.from_object('config')

app.config['SQLALCHEMY_DATABASE_URI'] = ''
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Models

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    handleid = db.Column(db.BigInteger, nullable=False)
    name = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return '<Model %r' % (self.id)

class Tweets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)

    tweetid = db.Column(db.BigInteger, nullable=False)
    author = db.Column(db.String(100), nullable=False)
    link = db.Column(db.Text, nullable=False)
    website = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False )
    handle = db.Column(db.BigInteger, nullable=False)  

    def __repr__(self):
        return '<Tweets %r' % (self.id)

oauth = OAuth(app)
oauth.register(
    name='twitter',
    api_base_url='https://api.twitter.com/1.1/',
    request_token_url='https://api.twitter.com/oauth/request_token',
    access_token_url='https://api.twitter.com/oauth/access_token',
    authorize_url='https://api.twitter.com/oauth/authenticate',
    fetch_token=lambda: session.get('token'),
)

def get_current_user():

    user_result = None

    if 'user' in session:
        hid = session['user']['id']
        user_result = User.query.filter_by(handleid=hid).first()

    return user_result

# Views

@app.errorhandler(OAuthError)
def handle_error(error):
    return render_template('error.html', error=error)


@app.route('/')
def homepage():
    user = session.get('user')

    if user:
        if bool(User.query.filter_by(handleid=user['id']).first()) is False:
            newuser = User(handleid = user['id'], name = user['screen_name'])
            db.session.add(newuser)
            db.session.commit()

    return render_template('index.html', user=user)


@app.route('/login')
def login():
    redirect_uri = url_for('auth', _external=True)
    return oauth.twitter.authorize_redirect(redirect_uri)


@app.route('/about')
def about():
    user = get_current_user()
    return render_template('about.html', user = user)


@app.route('/auth')
def auth():
    token = oauth.twitter.authorize_access_token()
    url = 'account/verify_credentials.json'
    resp = oauth.twitter.get(url, params={'skip_status': True})
    user = resp.json()

    session['token'] = token
    session['user'] = user
    return redirect('/')


@app.route('/logout')
def logout():
    session.pop('token', None)
    session.pop('user', None)
    return redirect('/')

@app.route('/analyze')
def analyze_tweets():
    user = get_current_user()

    if user:
        maxtweet = db.session.query(Tweets.author, db.func.count(Tweets.text)).filter(Tweets.handle==user.handleid).group_by(Tweets.author).order_by(db.func.count(Tweets.text).desc()).limit(1).all()
        maxlink = db.session.query(Tweets.website, db.func.count(Tweets.text)).filter(Tweets.handle==user.handleid).group_by(Tweets.website).order_by(db.func.count(Tweets.website).desc()).all()
    
        return render_template('analyze.html', links = maxlink, authors = maxtweet)

    else:

        return redirect(url_for('homepage', user=user))


@app.route('/tweets')
def list_tweets():
    user = get_current_user()

    url = 'statuses/home_timeline.json'
    params = {'include_rts': 0, 'count': 200, 'tweet_mode':'extended'}
    prev_id = request.args.get('prev')
    if prev_id:
        params['max_id'] = prev_id

    resp = oauth.twitter.get(url, params=params)
    tweets = resp.json()

    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"

    for i in range(len(tweets)):
        mytext = tweets[i]['full_text']
        url = re.findall(regex, mytext)

        currdate = tweets[i]['created_at']
        currobj = datetime.strptime(currdate,'%a %b %d %H:%M:%S +0000 %Y')

        if url and currobj > sevendays :
            
            if bool(Tweets.query.filter_by(tweetid=tweets[i]['id']).first()) is False:

                finalurl = tweets[i]['entities']['urls']

                if finalurl:        

                    parsed_uri = finalurl[0]['expanded_url']
                    r = requests.get(parsed_uri) 
                    finaldest = r.url

                    dom = urlparse(finaldest)
                    domain = '{uri.netloc}/'.format(uri=dom)

                    newtweet = Tweets(text = tweets[i]['full_text'], tweetid = tweets[i]['id'], author = tweets[i]['user']['screen_name'], link = finaldest, website = domain, created_at = currobj, handle = user.handleid)
                    db.session.add(newtweet)

                    db.session.commit()

                else:
                    continue
            else:
                continue

        elif currobj > sevendays:
            continue
        else:
            break

    op = Tweets.query.filter(Tweets.handle==user.handleid and Tweets.created_at>sevendays).order_by(Tweets.id.desc()).all()
    return render_template('tweets.html', lasttweet = tweets[-1], tweets=op)

@app.errorhandler(404)
def not_found(error):
  return render_template('error.html', error=error)

if __name__ == '__main__':
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.run()

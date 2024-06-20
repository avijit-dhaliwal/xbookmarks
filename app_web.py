from flask import Flask, redirect, url_for, session, render_template, request
from dotenv import load_dotenv
import os
import tweepy

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

# Twitter OAuth setup
auth = tweepy.OAuth1UserHandler(
    os.getenv('TWITTER_CONSUMER_KEY'),
    os.getenv('TWITTER_CONSUMER_SECRET'),
    os.getenv('TWITTER_CALLBACK_URL')
)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login')
def login():
    redirect_url = auth.get_authorization_url()
    session['request_token'] = auth.request_token
    return redirect(redirect_url)

@app.route('/callback')
def callback():
    request_token = session.pop('request_token', None)
    auth.request_token = request_token
    auth.get_access_token(request.args.get('oauth_verifier'))
    api = tweepy.API(auth)
    user_info = api.me()._json
    session['twitter_id'] = user_info['id_str']
    session['username'] = user_info['screen_name']
    return redirect(url_for('bookmarks'))

@app.route('/bookmarks')
def bookmarks():
    twitter_id = session.get('twitter_id')
    if not twitter_id:
        return redirect(url_for('login'))
    # Fetch bookmarks from Twitter or database
    bookmarks = [{'text': 'Example Bookmark 1'}, {'text': 'Example Bookmark 2'}]  # Example data
    return render_template('bookmarks.html', bookmarks=bookmarks)

@app.route('/update_email', methods=['POST'])
def update_email():
    data = request.json
    email = data.get('email')
    # Update email logic
    return {'status': 'success', 'message': 'Email updated successfully.'}

if __name__ == '__main__':
    app.run(debug=True)

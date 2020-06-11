from twython import Twython
import tweepy
from sqlalchemy.engine import create_engine
from .preprocess import preprocess
import json
import random, datetime, time
import tweepy

# Setup API Keys
app_key = "iSARkiEMiRNpyIt4z0ksLdEgA"
app_secret = "FCeXPjkJkiNPByAT3QtDyoTdV0Uq4msJgdFWtk7e34uANA5VeP"
oauth_token = "855516187538604032-85HhQucyZJd34U4vxNZb6CT4H7Lh1iU"
oauth_token_secret = "yUm4a4DPN12YxZ9PFv9CvgGH1eyexWUjoacz2yCA8LIsZ"
twitter = tweepy.OAuthHandler(
    app_key, app_secret
)
twitter.set_access_token(oauth_token, oauth_token_secret)

api = tweepy.API(twitter, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
twitter = Twython(app_key, app_secret, oauth_token, oauth_token_secret)

def search_by_id(id):
    result = api.get_status(id)
    # print('search_by_id',result)
    return result


# see https://dev.twitter.com/rest/reference/get/search/tweets for search options
def search(param, count=100):
    results = twitter.search(q=param, count=count)
    query_res = []
    for tweet in results['statuses']:
        # print(json.dumps(tweet))
        body = tweet['text']
        postid = tweet['id']
        timestamp = datetime.datetime.strptime(tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y').strftime('%Y-%m-%d %H:%M:%S')
        location = tweet['user']['location']
        userid = tweet['user']['id']
        username = tweet['user']['screen_name']
        query_res.append(tweet)
        body = preprocess(body)
        # print(username, body, end='\n\n')
    return query_res
        # Pass body to model and fetch has_bullying
        # Insert entry into db table

if __name__ == '__main__':
    # TODO:
    # Setup a cron job for hourly running this script
    # Allow to configure this through web gui
    search('#racism', 1)

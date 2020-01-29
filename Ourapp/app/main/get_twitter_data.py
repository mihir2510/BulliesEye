import tweepy
from sqlalchemy.engine import create_engine
from preprocess import preprocess
from model import predict
import random, datetime, time, pprint

CONSUMER_KEY = "iSARkiEMiRNpyIt4z0ksLdEgA"
CONSUMER_SECRET = "FCeXPjkJkiNPByAT3QtDyoTdV0Uq4msJgdFWtk7e34uANA5VeP"
OAUTH_TOKEN = "855516187538604032-85HhQucyZJd34U4vxNZb6CT4H7Lh1iU"
OAUTH_TOKEN_SECRET = "yUm4a4DPN12YxZ9PFv9CvgGH1eyexWUjoacz2yCA8LIsZ"
twitter = tweepy.OAuthHandleselecr(
    CONSUMER_KEY, CONSUMER_SECRET
)
twitter.set_access_token(OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
api = tweepy.API(twitter, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
engine = create_engine('sqlite:///../../database.db')
conn = engine.connect()

def search(param, count=100):
    bcount, tcount = 0, 0
    tic = time.time()
    print('Sending request...')
    for tweet in tweepy.Cursor(api.search, q=param, tweet_mode='extended').items(count):
        # print(pprint.pprint(tweet._json))
        
        tweet = tweet._json
        tweet_id = tweet['id']
        body = tweet['full_text']
        created_at = tweet['created_at']
        username = tweet['user']['screen_name']
        location = tweet['user']['location']

        # Preprocess body
        pbody = ' '.join(preprocess(body))
        labels, has_bullying, score = predict(pbody)
        if has_bullying:
            bcount += 1
            print(body, labels, has_bullying, end='\n\n')
        tcount += 1
    
        conn.execute("INSERT INTO Tweets VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)", (tweet_id, body, created_at, username, location, pbody, has_bullying, labels, score,))
        print('Inserted...')
    tac = time.time()
    print(100 * (bcount / tcount), 'Time taken', tac - tic)

if __name__ == '__main__':
    # TODO:
    # Setup a cron job for hourly running this script
    # Allow to configure this through web gui
    search('obama', 1000)
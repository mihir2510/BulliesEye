from twython import Twython
from sqlalchemy.engine import create_engine
import random, datetime, time

#Setup API Keys
app_key = "iSARkiEMiRNpyIt4z0ksLdEgA"
app_secret = "FCeXPjkJkiNPByAT3QtDyoTdV0Uq4msJgdFWtk7e34uANA5VeP"
oauth_token = "855516187538604032-85HhQucyZJd34U4vxNZb6CT4H7Lh1iU"
oauth_token_secret = "yUm4a4DPN12YxZ9PFv9CvgGH1eyexWUjoacz2yCA8LIsZ"

twitter = Twython(app_key, app_secret, oauth_token, oauth_token_secret)

engine = create_engine("sqlite:///../cbd_project/cyber.sqlite3")
conn = engine.connect()

# see https://dev.twitter.com/rest/reference/get/search/tweets for search options
results = twitter.search(q="#GoT", count=100)
for tweet in results['statuses']:
    body = tweet['text']
    postid = tweet['id']
    timestamp = datetime.datetime.strptime(tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y').strftime('%Y-%m-%d %H:%M:%S')
    location = tweet['user']['location']
    userid = tweet['user']['id']
    username = tweet['user']['screen_name']
    # print (postid, timestamp, location, userid, username, body, end='\n\n')
    has_bullying = random.choice(['Yes', 'No'])
    
    sql = f"""INSERT INTO cbd_processedsocialmediamessage(postid, body, date, username, location, has_bullying) VALUES ({postid}, "{body}", "{timestamp}", "{username}", "{location}", "{has_bullying}")"""
    print(sql, end='\n\n')
    tid = conn.execute(sql)
    print('Done', tid)


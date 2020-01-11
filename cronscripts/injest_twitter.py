from twython import Twython

#Setup API Keys
app_key = "iSARkiEMiRNpyIt4z0ksLdEgA"
app_secret = "FCeXPjkJkiNPByAT3QtDyoTdV0Uq4msJgdFWtk7e34uANA5VeP"
oauth_token = "855516187538604032-85HhQucyZJd34U4vxNZb6CT4H7Lh1iU"
oauth_token_secret = "yUm4a4DPN12YxZ9PFv9CvgGH1eyexWUjoacz2yCA8LIsZ"

twitter = Twython(app_key, app_secret, oauth_token, oauth_token_secret)

# see https://dev.twitter.com/rest/reference/get/search/tweets for search options
results = twitter.search(q="#GoT", count=100)
for tweet in results['statuses']:
    body = tweet['text']
    id = tweet['id']
    timestamp = tweet['created_at']
    location = tweet['user']['location']
    userid = tweet['user']['id']
    username = tweet['user']['screen_name']
    print (id, timestamp, location, userid, username, body)

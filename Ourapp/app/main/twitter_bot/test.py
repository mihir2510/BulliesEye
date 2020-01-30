import tweepy

CONSUMER_KEY = "iSARkiEMiRNpyIt4z0ksLdEgA"
CONSUMER_SECRET = "FCeXPjkJkiNPByAT3QtDyoTdV0Uq4msJgdFWtk7e34uANA5VeP"
OAUTH_TOKEN = "855516187538604032-85HhQucyZJd34U4vxNZb6CT4H7Lh1iU"
OAUTH_TOKEN_SECRET = "yUm4a4DPN12YxZ9PFv9CvgGH1eyexWUjoacz2yCA8LIsZ"
twitter = tweepy.OAuthHandler(
    CONSUMER_KEY, CONSUMER_SECRET
)
twitter.set_access_token(OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
api = tweepy.API(twitter)

try:
    api.verify_credentials()
    print("Authentication OK")
except:
    print("Error during authentication")
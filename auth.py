import tweepy
import settings
import sys, os
import datetime
import subprocess
import pickle

class loadTweets(object):
   
    def fetchTweets(self, since_id=None):
        if since_id:
            tweets = self.api.home_timeline(since_id, count=100)
        else:
            tweets = self.api.home_timeline(count=100)
        # parse each incoming tweet
        ts = []
        authors = []
        for tweet in tweets: 
            t = {
            'author': tweet.author.screen_name,
            'contributors': tweet.contributors,
            'coordinates': tweet.coordinates,
            'created_at': tweet.created_at,
            # 'destroy': tweet.destroy,
            # 'favorite': tweet.favorite,
            'favorited': tweet.favorited,
            'geo': tweet.geo,
            'id': tweet.id,
            'in_reply_to_screen_name': tweet.in_reply_to_screen_name,
            'in_reply_to_status_id': tweet.in_reply_to_status_id,
            'in_reply_to_user_id': tweet.in_reply_to_user_id,
            # 'parse': tweet.parse,
            # 'parse_list': tweet.parse_list,
            'place': tweet.place,
            # 'retweet': dir(tweet.retweet),
            # 'retweets': dir(tweet.retweets),
            'source': tweet.source,
            # 'source_url': tweet.source_url,
            'text': tweet.text,
            'truncated': tweet.truncated,
            'user': tweet.user.screen_name,
            }
            u = {
            '_id': tweet.author.screen_name, # use as mongo primary key
            'contributors_enabled': tweet.author.contributors_enabled, 
            'created_at': tweet.author.created_at, 
            'description': tweet.author.description, 
            'favourites_count': tweet.author.favourites_count, # beware the british
            'follow_request_sent': tweet.author.follow_request_sent, 
            'followers_count': tweet.author.followers_count, 
            'following': tweet.author.following, 
            'friends_count': tweet.author.friends_count, 
            'geo_enabled': tweet.author.geo_enabled, 
            'twitter_user_id': tweet.author.id, 
            'lang': tweet.author.lang, 
            'listed_count': tweet.author.listed_count, 
            'location': tweet.author.location, 
            'name': tweet.author.name, 
            'notifications': tweet.author.notifications, 
            'profile_image_url': tweet.author.profile_image_url, 
            'protected': tweet.author.protected, 
            'statuses_count': tweet.author.statuses_count, 
            'time_zone': tweet.author.time_zone, 
            'url': tweet.author.url, 
            'utc_offset': tweet.author.utc_offset, 
            'verified': tweet.author.verified,
            '_updated': datetime.datetime.now(),
            }
            authors.append(u)
            ts.append(t)        
        
        # insert into db
        try:
            print ts
        except pymongo.errors.InvalidOperation: # no tweets?
            pass
        
        if self.debug:
            print "added %s tweets to the db" % (len(ts))
    def __init__(self, debug=False):
        self.debug = debug
        auth = tweepy.OAuthHandler(settings.CONSUMER_KEY, settings.CONSUMER_SECRET)
        auth.set_access_token(settings.ACCESS_KEY, settings.ACCESS_SECRET)
        self.api = tweepy.API(auth)

        try:
            self.fetchTweets()
        except tweepy.error.TweepError: # authorization failure
            print "You need to authorize tc to connect to your twitter account. I'm going to open a browser. Once you authorize, I'll ask for your PIN."
            auth = self.setup_auth()
            self.api = tweepy.API(auth)
            self.fetchTweets()
        

    # util classes    
    def setup_auth(self):
        """
        setup_auth: authorize tc with oath
        """
        auth = tweepy.OAuthHandler(settings.CONSUMER_KEY, settings.CONSUMER_SECRET)
        auth_url = auth.get_authorization_url()
        p = subprocess.Popen("open %s" % auth_url, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        print "( if the browser fails to open, please go to: %s )" % auth_url
        verifier = raw_input("What's your PIN: ").strip()
        auth.get_access_token(verifier)
        pickle.dump((auth.access_token.key, auth.access_token.secret), open('settings_twitter_creds','w'))        
        return auth
    
    def init_twitter(self, username, password):
        auth = tweepy.BasicAuthHandler(username, password)
        api = tweepy.API(auth)
        return api


if __name__ == '__main__':
    l = loadTweets(debug=True)

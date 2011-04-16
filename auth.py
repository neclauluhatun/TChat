import tweepy
import settings
import sys, os
import datetime
import subprocess
import pickle
import thread

class loadTweets(object):
    lastID=0
    def sendMessages(self,userName):
        while 1:
            message = str(raw_input("message?\n"))
            self.api.send_direct_message(screen_name = userName, text = message)
    def getMessage(self,userName):
        while 1:
            if ID:
                mesajlar = self.api.direct_messages(since_id=lastID,count=10)
            else:
                mesajlar = self.api.direct_messages(count=10)
            for msg in mesajlar:
                if msg.sender.screen_name == userName and msg.created_at > datetime.datetime(2011, 4, 15, 23, 36, 2):
                    print "Mesaj geldi = %s !" % msg.text
                    self.lastID=msg.id
    def fetchTweets(self, since_id=None):
        if since_id:
            tweets = self.api.home_timeline(since_id, count=10)
        else:
            #tweets = self.api.home_timeline(screen_name="ozansener",count=10)
            tweets = self.api.mentions(count=10)
        followers = self.api.followers(screen_name='msencer')
        # parse each incoming tweet
        ts = []
        users={}
        authors = []
##        for tweet in tweets:
##           if tweet.author.screen_name=="ozansener" :
##            print str(tweet.in_reply_to_status_id) + "\n"
##            t = {
##            'author': tweet.author.screen_name,
##            # 'destroy': tweet.destroy,
##            # 'favorite': tweet.favorite,
##            'id': tweet.id,
##            'in_reply_to_screen_name': tweet.in_reply_to_screen_name,
##            'in_reply_to_status_id': tweet.in_reply_to_status_id,
##            'in_reply_to_user_id': tweet.in_reply_to_user_id,
##            # 'parse': tweet.parse,
##            # 'parse_list': tweet.parse_list,
##            # 'retweet': dir(tweet.retweet),
##            # 'retweets': dir(tweet.retweets),
##            # 'source_url': tweet.source_url,
##            'text': tweet.text,
##            'created': tweet.created_at,
##            'user': tweet.user.screen_name,
##            }
##            u = {
##            '_id': tweet.author.screen_name, # use as mongo primary key
##            'contributors_enabled': tweet.author.contributors_enabled, 
##            'created_at': tweet.author.created_at, 
##            'description': tweet.author.description, 
##            'favourites_count': tweet.author.favourites_count, # beware the british
##            'follow_request_sent': tweet.author.follow_request_sent, 
##            'followers_count': tweet.author.followers_count, 
##            'following': tweet.author.following, 
##            'friends_count': tweet.author.friends_count, 
##            'geo_enabled': tweet.author.geo_enabled, 
##            'twitter_user_id': tweet.author.id, 
##            'lang': tweet.author.lang, 
##            'listed_count': tweet.author.listed_count, 
##            'location': tweet.author.location, 
##            'name': tweet.author.name, 
##            'notifications': tweet.author.notifications, 
##            'profile_image_url': tweet.author.profile_image_url, 
##            'protected': tweet.author.protected, 
##            'statuses_count': tweet.author.statuses_count, 
##            'time_zone': tweet.author.time_zone, 
##            'url': tweet.author.url, 
##            'utc_offset': tweet.author.utc_offset, 
##            'verified': tweet.author.verified,
##            '_updated': datetime.datetime.now(),
##            }
##            authors.append(u)
##            ts.append(t)        
##        print ts
        print "Select a user:\n"
        i=0
        for fw in followers:
            i+=1
            print "%d - %s" % (i,fw.screen_name)
            users[i]=fw.screen_name
        choice = int(raw_input("make your choice?\n"))
        
        #try:
        deger = str(users[choice])
        #self.getMessage(deger)
        thread.start_new_thread(self.sendMessages,(deger,))
        thread.start_new_thread(self.getMessage,(deger,))

        #except:
          #  print "Error: unable to start thread"
        
        
        
##        self.TweetAMessage()
            #self.api.send_direct_message("ozansener","selamlar")
    def TweetAMessage(self):
        self.api.send_direct_message(screen_name = "ozansener", text = "selamlar")
        #self.api.update_status(status="hackABit test",in_reply_to_status_id=54622552307412992)
        #self.api.retweet(54622552307412992L)
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

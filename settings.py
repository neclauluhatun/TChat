
# configure me!
TWITTER_USERNAME = 'hackAbitCS'

# you shouldn't need to touch

import pickle

CONSUMER_KEY = 'TvX0eTEYAN6YoytH0azwA'
CONSUMER_SECRET = 'uvmnKziQfawPrKaLUKBgHlpPx8OhJ9RyCx5oi8Kg'

KLOUT_API_KEY = 'TvX0eTEYAN6YoytH0azwA'

try:
    (ACCESS_KEY, ACCESS_SECRET) = pickle.load(open('settings_twitter_creds'))
except IOError:
    (ACCESS_KEY, ACCESS_SECRET) = ('', '')

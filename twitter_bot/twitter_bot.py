""" Our Twitter bot!

Authors: Mariarosa, Timmy, Ania, Eli, Oli
"""

import numpy as np  # an http library written for humans
import tweepy

#This is going to return a quote test in the first instance


def get_quote():
    quotes = ["That's no moon!",
              "I suppose this will all make sense when we grow up.",
              "Life before death.",
              "Supercalifragilisticexpialidocious"]
    authors = ['Obi Wan Kenobi', 'Calvin', 'Kaladin', 'Mary Poppins']
    idx = np.random.randint(len(quotes))
    return quotes[idx] + ' - ' + authors[idx]

def send_tweet():
    tweet = get_quote()
    # status = api.update_status(tweet)
    # print(status.id)
    print(tweet)

if __name__ == '__main__':
    send_tweet()


        # ## Todo: get approved for twitter api use
        # consumer_key = YOUR CONSUMER KEY
        # consumer_secret = YOUR CONSUMER SECRET
        # access_token = YOUR ACCESS TOKEN
        # access_token_secret = YOUR ACCESS TOKEN SECRET
        #
        # # Twitter requires oAuth2 to access its API:
        # auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        # auth.set_access_token(access_token, access_token_secret)
        # api = tweepy.API(auth)
        #
        # tweet = get_quote()

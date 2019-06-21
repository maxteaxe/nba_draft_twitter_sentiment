""" connect.py

contains functions necessary to connect to API's

This file contains functions
    * twitter_api() - connect to the twitter API

Created by Ben Capodanno June 21, 2019. Updated June 21, 2019.
"""

import tweepy
import os

def twitter_api():
    """ function used to authorize Twitter API

    :returns: API object that allows for Twitter API access
    :rtype: Tweepy API object
    """

    auth = tweepy.OAuthHandler( os.environ['TWITTER_API'], os.environ['TWITTER_API_SECRET'] )
    auth.set_access_token( os.environ['TWITTER_ACCESS'], os.environ['TWITTER_ACCESS_SECRET'] )

    return tweepy.API( auth )
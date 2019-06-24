""" access.py

functions to save and access both saved and web based tweets

This file contains functions:
    * get_save_tweets( filepath, api, query, max_tweets, lang ) - Gets tweets based on a query and 
                                                                  converts to JSON format
    * access_saved_tweets( filepath ) - converts JSON formatted tweets to Pandas df
    * extract_tweet( filepath, id ) - extracts a specific tweet, based on its ID, from a JSON tweet file
    * main() - This files main function, ensures functionality of above


Created by Ben Capodanno & TK Kwon on June 22, 2019. Updated June 23, 2019
"""

import sys
import jsonpickle as jp
import connect as cn
import tweepy as tp
import pandas as pd

def get_save_tweets(filepath, api, query, max_tweets=10000, lang='en'):
    """ gets tweets from twitter and saves to JSON file

    :param filepath: The path of the file to save the tweets to
    :type filepath: String
    :param api: Thhe API through which to access the tweets
    :type API: Tweepy API Object
    :param query: The query by which the search is executed
    :type query: String
    :param max_tweets: The maximum number of tweets to return in the search
    :type max_tweets: int
    :param lang: Thee language of the tweets
    :type lang: String
    :returns: None
    :rtype: None
    """

    tweetCount = 0

    #Open file and save tweets
    with open(filepath, 'w') as f:

        print( "Saving queried tweets..." )
        # Send the query
        for tweet in tp.Cursor(api.search,q=query,lang=lang).items(max_tweets):    

            #Convert to JSON format
            f.write( jp.encode(tweet._json, unpicklable=False) + '\n' )
            tweetCount += 1

        #Display how many tweets we have collected
        print("Downloaded {0} tweets".format(tweetCount))
    
    return

def access_saved_tweets( filepath ):
    """ forms a pandas df out of a tweet file

    :param filepath: The tweet file json to parse
    :type filepath: String
    :returns: A df containing all tweets and their metadata from a file
    :rtype: Pandas Data Frame
    """
    print( "Accessing JSON..." )

    tweets = list( open( filepath, 'rt' ) )
    
    id_str = []
    text = []
    verified = []
    follower = []
    description = []

    for t in tweets:
        t = jp.decode( t )
        
        # Tweet identifier
        id_str.append( t['id_str'] )

        # Text
        text.append( t['text'] )
        
        verified.append( t['user']['verified'] )

        # Followers number
        follower.append( t['user']['followers_count'] )
        
        # Add user bio
        description.append( t['user']['description'] )
        
    d = {'id_str': id_str,
         'text': text,
         'verified': verified,
         'followers': follower,
         'description' : description
        }
    
    return pd.DataFrame( data = d )

def extract_tweet( filepath, id ):
    """ extracts a tweet based on its ID from a json file

    :param filepath: The location of the JSON file
    :type filepath: String
    :param id: The unique ID of the tweet
    :type id: String
    :returns: The decoded tweet, or None if it is not present
    :rtype: Dictionary or None
    """

    tweets = list( open( filepath, 'rt' ) )

    for t in tweets:
        t = jp.decode( t )

        if t['id_str'] == id:
            return t

    return

def main():
    """ access and save tweets for a given query

    :returns: None
    :rtype: None
    """

    filepath = "test.json"
    query = "#testing123"

    api = cn.twitter_api()
    get_save_tweets( filepath, api, query )
    df = access_saved_tweets( filepath )
    print( df.head() )
    et = extract_tweet( filepath, df.iloc[4]["id_str"] )
    print( et["id_str"] )

if __name__ == "__main__":
    if len( sys.argv ) > 1:
        print( "USAGE: python access.py" )
        exit()
    main()

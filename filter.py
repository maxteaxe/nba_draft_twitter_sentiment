import pandas as pd 
import access
import connect as cn
import sys

def follower_count_filter(count, dataframe : pd.DataFrame):
    df = dataframe.loc[dataframe["followers"] > count]
    return df


def description_filter(text : str, dataframe : pd.DataFrame):

    df = dataframe
    
    df = df[df["description"].str.contains(text)]

    return df

def main():
    """ access and save tweets for a given query

    :returns: None
    :rtype: None
    """
    filepath = "test2.json"
    query = "#testing123"

    api = cn.twitter_api()
    access.get_save_tweets( filepath, api, query )
    df = access.access_saved_tweets( filepath )
    
    filtered = follower_count_filter(200, df)
    filtered2 = description_filter("love", filtered)


    

if __name__ == "__main__":
    if len( sys.argv ) > 1:
        print( "USAGE: python access.py" )
        exit()
    main()
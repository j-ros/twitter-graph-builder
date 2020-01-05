# -*- coding: utf-8 -*-
"""
Created on Sat Nov 16 17:16:56 2019

@author: Jesús Ros Solé

Script to download Twitter tweets using Tweepy StreamListener.
Data is stored in a local MongoDB database. Process must be interrupted when
enough data has been fetched.

Variables to define:
    - consumer_key, consumer_secret, access_token and access_token_secret
        Authentification tokens from Twitter API.
    - database and collection
        Name of the database and collection in the local MongoDB database.
    - hashtags
        List with the hashtags to follow.
"""

import json
from pymongo import MongoClient
import tweepy


def get_auth(consumer_key, consumer_secret, access_token, access_token_secret):
    """
	Returns an OAuthHandler object with the authentification credentials.
    """
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    return auth


class StreamListener(tweepy.StreamListener):
    """
	Extends Tweepy StreamListener to store data in local MongoDB database.
    """
    
    def __init__(self, api=None, database='test', collection='test'):
        """
        Constructor
        
        api: object with authenitification credentials for the Twitter API.
        database: name of the local database in MongoDB.
        collection: name of the local collection in MongoDB.
        db: object with the instance of the MongoDB connection.
        """
        super(tweepy.StreamListener, self).__init__()
        self.database = database
        self.collection = collection
        self.db = MongoClient()[database][collection]

    def on_connect(self):
        """
		Prints information about the sucess of the connection to the Twitter API
		and the local MongoDB connection.
		
		Called at the start of the stream connection.
        """
        print("Twitter streaming API connected.",
              "Storing tweets in local database \'" + self.database +
              "\' and collection \'" + self.collection + "\'.", sep='\n')
 
    def on_error(self, status_code):
        """
		Prints error messages and closes the stream on error.
		
		Called on stream error.
        """
        print('An Error has occured: ' + repr(status_code))
        return False # Disconnect the stream
 
    def on_data(self, data):
        """
		Called every time a new tweet arrives. Stores the json of the tweet in the
		local MongoDB connection o returns an exception if one happens.
        """
        try:
            self.db.insert_one(json.loads(data))
        except Exception as e:
            print(e)


if __name__ == '__main__':
    # Twitter keys
    consumer_key = ''
    consumer_secret = ''
    access_token = ''
    access_token_secret = ''
    
    # MongoDB
    database = ''
    collection = ''
    
    # Hashtags
    hashtags = [''] 

    # Authentification
    auth = get_auth(consumer_key, consumer_secret, access_token, access_token_secret)
    
    # Start the stream
    streamer = tweepy.Stream(auth=auth, 
                             listener=StreamListener(api=tweepy.API(wait_on_rate_limit=True),
                                                     database=database, collection=collection))
    streamer.filter(track=hashtags)
    
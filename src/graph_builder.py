# -*- coding: utf-8 -*-
"""
Created on Sat Nov 16 18:40:31 2019

@author: Jesús Ros Solé

Script to create a graph from Twitter data in a local MongoDB database.

The graph is created from users (nodes) and replies, quotes and retweets between
users (edges). If a user A tweets a reply, quote or retweet on user B an edge between 
both nodes is created or its weight incremented by 1, if the edge existed.

Variables to define:
    - database and collection
        Name of the database and collection in the local MongoDB database.
    - filename
        Name of the resulting graphml file.
"""

from pymongo import MongoClient
import networkx as nx


class GraphBuilder():
    """
	Class to fetch tweets from local MongoDB and build a directed graph with 
	weights from replies, quotes and retweets between users.
    """
    def __init__(self, database='test', collection='test'):
        """
        Constructor
        
        database: name of the local database in MongoDB.
        collection: name of the local collection in MongoDB.
        db: object with the instance of the MongoDB connection.
        G: empty directed graph.
        """
        self.database = database
        self.collection = collection
        self.db = MongoClient()[database][collection]
        self.G = nx.DiGraph()
    
    def _update_edge_weight(self, node_from, node_to):
        """
		Creates an edge between node_from and node_to nodes or increases
		its weight by 1, if it already exists.
        """
        if self.G.has_edge(node_from, node_to):
            self.G[node_from][node_to]['weight'] += 1
        else:
            self.G.add_edge(node_from, node_to, weight=1 )

    def build_graph(self):
        """
		Fetches tweets from local MongoDB connection one by one and extracts 
		the screen_name of the author as well as the screen_name of the reply,
		quote or retweet objective, if it exists. Then calls the function to
		update weights accordingly.
        """
        for tweet in self.db.find():
            user_from = tweet['user']['screen_name']
            self.G.add_node(user_from)
            keys = tweet.keys()
            if tweet['in_reply_to_screen_name'] is not None:
                user_to = tweet['in_reply_to_screen_name']
                self._update_edge_weight(user_from, user_to)
            if 'quoted_status' in keys:
                user_to = tweet['quoted_status']['user']['screen_name']
                self._update_edge_weight(user_from, user_to)
            if 'retweeted_status' in keys:
                user_to = tweet['retweeted_status']['user']['screen_name']
                self._update_edge_weight(user_from, user_to)
    
    def export_graph(self, filename):
        """
		Creates a graphml file with the resulting graph.
        """
        nx.write_graphml(self.G, filename)
        

if __name__ == '__main__':
    # MongoDB
    database = ''
    collection = ''
    
    # Graphml
    filename = ''
    
    graf = GraphBuilder(database, collection)
    graf.build_graph()
    graf.export_graph(filename)
     
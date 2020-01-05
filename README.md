# Twitter Graph Builder
### Author: Jesús Ros Solé

## Objective

The objective of this project is to obtain a graph representation of data extracted from Twitter. Data is stored in a MongoDB local database for processing.

The project is developed in Python3 and uses the following external libraries:
- json
- MongoClient, from PyMongo
- tweepy
- networkx

## Content

- src
  - streamer.py: Python script that captures data from a Tweeter Stream and stores the data in a local MongoDB database.
  - graph_builder.py: Python script that fetches data from a local MongoDB database and builds a graphml file with the resulting directed graph with weights, taking replies, quotes and retweets as relations.
- LICENCE: license file under which this work is released.
- README.md: this file.

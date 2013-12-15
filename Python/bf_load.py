"""This module interfaces with MongoDB and can pickle networkx objects
It is designed to do all of the database i/o for the project"""

import json
import pickle
import networkx as nx
from pymongo import MongoClient
from datetime import datetime

###################  MAIN TWEET FILE -- EACH LINE IS A JSON OBJECT     ################
file = open('../../../../Documents/Boulder_Floods/boulder_floods.json', 'r')
db = MongoClient().mydb.tweets	#Main Collection
#######################################################################################
##################################   POPULAR QUERIES     ##############################
only_geo_tagged = {	'spec': {'geo': {'$ne': None }},	#Only geolocated tweets?
					'fields':{	'_id'			:	0, 
								'id'			:	1, 
								'user.screen_name': 1,
								'text'			:	1,
								'user.id'		:	1, 
								'entities.user_mentions':1} }
all_tweets = {		'spec':	 {},                            # All Tweets, no filters
					'fields':{	
						'_id'                   : 0,        # This is the Mongo ID 
						'id'                    : 1,        # This is a number
						'user.screen_name'      : 1,        # For the label
						'user.id'               : 1,        # User ID (node ID)
						'created_at'			: 1,        # Date Object
						'entities'				: 1} }      # For User Mentions/Hashtags

#######################################################################################

def populate_mongoDB():
	"""Populates the MongoDB by parsing each line of the .json ile as text fa JSON object.
	Takes special care to convert the created_at field"""
	global file, db
	counter = 0
	for line in file:               # Standard iteration through file
		tweet = json.loads(line)    # Recognize it as a JSON object
		tweet['created_at'] = datetime.strptime(tweet['created_at'].replace('+0000',''),
			'%a %b %d %H:%M:%S %Y')
		db.insert(tweet)            # Actually insert it into the tweets collection
		if counter % 10000 == 0:    # Shows import update status - can take a while
			print counter,
		counter += 1
	print "done"

def query_mongo_get_list(query = {} , limit=False):
	"""Returns array of tweet objects that match query, with fields specified by query.  

	|  Options:
	|  No Limit:  Returns array of all tweets
	|  Limit set: Returns array of size limit
	|  Limit==1:  Returns single tweet, not in array.
	"""
	global db
	if not limit:
		return list(db.find(spec=query['spec'], fields=query['fields']))
	elif limit==1:
		return list(db.find(spec=query['spec'], fields=query['fields']).limit(1))[0]
	else:
		return list(db.find(spec=query['spec'], fields=query['fields']).limit(limit))

def pickle_this(object_to_pickle, name):
	"""Pickles the object passed to it with the name passed and writes to pickle directory.

	|  Rarely implemented because for most graphs it is quicker to make real-time query.
	|  If graph requires making many queries, best to pickle the graph once it is made.
	"""
	print "Pickling ", str(name), '...',
	output = open('pickles/'+str(name)+'.pickle', 'wb')
	pickle.dump(object_to_pickle, output)
	print "done"

def unpickle_this(path):					#Deprecated in final version: too slow
	"""Reads the pickled data from the *pickle_this()* function.

	|  Rarely implemented because most graphs do not use the *pickle_this()*
	"""
	print "Unpickling "+str(path)+"...",
	this_obj = pickle.load(open('pickles/'+str(path)+'.pickle'))
	print "done"
	return this_obj

if __name__ == '__main__':               # If this file is called direclty, run import
	print "Running Import..."
	#populate_mongoDB()                  # ONLY RUN ONCE; COMMENTED OUT FOR SAFETY
	print "done"

"""Jennings Anderson 2013
CSCI 5352: Final Project: Boulder Flooding Twitter Network Analysis

This module interfaces with MongoDB and can pickle networkx objects
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

def populate_mongoDB():
	'''	Populates the MongoDB by parsing each line of the .json text file as a JSON object.
		Takes special care to convert the created_at field'''
	global file, db
	counter = 0
	for line in file:				# Standard iteration through file
		tweet = json.loads(line) 	# Recognize it as a JSON object
		tweet['created_at'] = datetime.strptime(tweet['created_at'].replace('+0000',''), '%a %b %d %H:%M:%S %Y')
		db.insert(tweet)			# Actually insert it into the tweets collection
		if counter % 10000 == 0:	# Show import update
			print counter,
		counter += 1

def query_mongo_get_list(query = {} , limit=False):	# Default just returns all
	'''	Returns array of tweets that match query, with fields specified by query.  
		Options:
			No Limit:  Returns array of all tweets
			Limit set: Returns array of size limit
			Limit==1:  Returns single tweet, not in array.'''
	global db
	if not limit:
		return list(db.find(spec=query['spec'], fields=query['fields']))
	elif limit==1:
		return list(db.find(spec=query['spec'], fields=query['fields']).limit(1))[0]
	else:
		return list(db.find(spec=query['spec'], fields=query['fields']).limit(limit))

def pickle_this(object_to_pickle, name):	#Deprecated in final version: too slow
	''' Pickles the object passed to it with the name passed and writes to pickle directory.
		Not used in final calculations because reading from database is faster than loading
		pickled file.'''
	print "Pickling ", str(name), '...',
	output = open('pickles/'+str(name)+'.pickle', 'wb')
	pickle.dump(object_to_pickle, output)
	print "done"

def unpickle_this(path):					#Deprecated in final version: too slow
	''' Reads the pickled data from the pickle_this() function.  Not implemented in final
		calculations because it is slower than reading from the database.'''
	print "Unpickling "+str(path)+"...",
	this_obj = pickle.load(open('pickles/'+str(path)+'.pickle'))
	print "done"
	return this_obj

if __name__ == '__main__':					# If this file is called direclty, then run import
	populate_mongoDB()

	If I make a change here, does it stick?

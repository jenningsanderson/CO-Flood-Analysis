"""Jennings Anderson 2013
CSCI 5352: Final Project: Boulder Flooding

This module creates a tweet of all users and their tweets.  It will be big."""

import bf_load as bf
import proj_funcs as f
import networkx as nx
import matplotlib.pyplot as plt
												# Syntax for what is returned, true/false
query = {	'spec': {}, # { 'geo' : {'$ne': None} },				# Only Geo-Tagged Tweets; for testing
			'fields':{	'_id'                   : 0,		# This is the Mongo ID 
						'id'                    : 1,		# This is a number
						'user.screen_name'      : 1, 		# 
						'user.id'               : 1, 		# User ID
						'text'					: 1, 		# We want the text of the tweet!
						'entities.user_mentions': 1} }		# Just in case...

def create_user_tweet_graph():
	counter=0
	tweets = bf.query_mongo_get_list(query)
	graph = nx.Graph()
	for tweet in tweets:
		user_id = int(tweet['user']['id'])	#Only care about the user.
		tweet_id = str(user_id)+'_tweet'

		if not graph.has_node(user_id):
			graph.add_node(user_id, type="user", label=tweet['user']['screen_name'].encode('ascii', 'ignore'), weight=1)
		
		if not graph.has_node(tweet_id):
			graph.add_node(tweet_id, type="tweet", weight=1, label="")

		if not graph.has_edge(user_id, tweet_id):	
			graph.add_edge(user_id, tweet_id, {'weight':1})
		else:
			graph[user_id][tweet_id]['weight']+=1
			graph.node[user_id]['weight']+=1
			graph.node[tweet_id]['weight']+=1

		counter+=1
		if counter%1000==0:
			print counter,
	return graph

graph = create_user_tweet_graph()				# This takes 8.7s
#graph = bf.unpickle_this('users_and_tweets')	# This takes 11.7 Seconds #

for node in graph.nodes():
	if graph.node[node]['weight'] < 10:
		graph.remove_node(node)

# print "Making full_hist graph"
# full_hist = f.bin_it(graph.degree())
# print len(full_hist)
# f.draw_graph(full_hist, scale='log', name='Degree_All_Nodes', style='go', sort=True, reverse=True )

# print "Making user_hist graph"
# node_type = nx.get_node_attributes(graph, 'type')
# user_hist = f.bin_it(graph.degree(), type="user", type_dict=node_type)
# print len(user_hist)
# f.draw_graph(user_hist, scale='log', name='Degree_Just_Users', style='ro', sort=True, reverse=True)

f.write_network_gml(graph, 'user_tweets_gt_10')
#Good - that works!
# print 'Making graph of ',len(graph.nodes()),'nodes and', len(graph.edges()), 'edges'
# f.draw_graph(histogram, style='ro', scale='log')

# The only reason is that first data point, which is really, really lame.






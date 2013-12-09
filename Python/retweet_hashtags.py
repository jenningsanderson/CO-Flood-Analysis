"""Jennings Anderson 2013
CSCI 5352: Final Project: Boulder Flooding

This module builds hashtag networks based on retweet frequency.
Hashtags are nodes and edges exist between them if they appear in the same tweet.
This is similar to a word cloud, but shows relation between tweets.

The hope is that by identifying clusters, SPAM keywords can be easily identified."""

import bf_load as bf
import proj_funcs as f
import networkx as nx
import matplotlib.pyplot as plt

query = {	'spec':	{'text':{'$regex':'^(RT|MT)'}},#, 'geo': {'$ne': None }},	#Only Geolocated tweets #For now.
			'fields':{	'_id':0, 'id':1, 'user.screen_name': 1, 'text':1,
						'user.id':1, 'entities.hashtags':1}
		}

def retweeted_graph(tweets_array):
	"""Returns graph from tweets array returned from mongoDB"""
	g = nx.Graph()
	counter = 0
	for tweet in tweets_array:
		counter += 1
		# Iterate through all hashtags array and add nodes if they don't exist yet.
	 	for hashtag in tweet['entities']['hashtags']:
	 		# Ignore unicode errors, python 2.7.5 (Source below)
	 		# http://stackoverflow.com/questions/3224268/python-unicode-encode-error
	 		tag = hashtag['text'].encode('ascii', 'ignore').lower()
	 		if not g.has_node(tag):
	 			g.add_node(tag, {'weight':0})
	 		else:
	 			g.node[tag]['weight'] += 1    #The weight is the number of times tag occurs
	 	
	 	# Now loop through entities again and grab all pairs of hashtags.
	 	for hashtag1 in tweet['entities']['hashtags']:
	 		tag1 = hashtag1['text'].encode('ascii', 'ignore').lower()
	 		for hashtag2 in tweet['entities']['hashtags']:
	 			tag2 = hashtag2['text'].encode('ascii', 'ignore').lower()
	 			
	 			# Add edges, but not self-loops between the edges
	 			if tag1 is not tag2 and not g.has_edge(tag1, tag2):
	 				g.add_edge(tag1, tag2, {'weight':0})
	 			elif tag1 is not tag2:
	 				g[tag1][tag2]['weight']+=1
	 	
	 	#So this works well, but what are edges going to be?

	 	if counter % 1000 == 0:							# For status update, can take a while
	 		print counter,
	 	#
	 	# this_tweet = str(tweet['text'])
	 	# mentions = tweet['entities']['user_mentions']
	 	# if user_tweet_counts.has_key(this_user):		# Count the tweets per user
	 	# 	user_tweet_counts[this_user] += 1
	 	# else:
	 	# 	user_tweet_counts[this_user] = 1
	 	# for j in mentions:								# Iterate through each user name in tweet
	 	# 	mention_id = str(j['screen_name'])
			# #http://stackoverflow.com/questions/3224268/python-unicode-encode-error					
	 	# 	g.add_edge(this_user, mention_id, label=tweet['id'])
	 	
	print "----DONE----"	
	return g

if __name__ == '__main__':
	retweets = bf.query_mongo_get_list(query)

	print len(retweets)	

	retweets_graph = retweeted_graph(retweets)

	pruned_graph = retweets_graph.copy()
	for node in pruned_graph.nodes():
		if pruned_graph.node[node]['weight'] < 500:
			pruned_graph.remove_node(node)

	#f.write_network_gml(pruned_graph, 'retweets_hashtag_gt30_lower')

	f.draw_network_plt(pruned_graph)

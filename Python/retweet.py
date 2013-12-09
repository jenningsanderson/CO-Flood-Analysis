"""Jennings Anderson 2013
CSCI 5352: Final Project: Boulder Flooding

This module handles visualzing retweeting of information within the network"""

import bf_load as bf
import proj_funcs as f
import networkx as nx
import matplotlib.pyplot as plt

query = {	'spec':	{'text':{'$regex':'^(RT|MT)'}},#'geo': {'$ne': None }},	#Only Geolocated tweets #For now.
			'fields':{	'_id':0, 'id':1, 'user.screen_name': 1, 'text':1,
						'user.id':1, 'entities.hashtags':1}
		}

retweets = bf.query_mongo_get_list(query)

print len(retweets)

def retweeted_graph(tweets_array):
	g = nx.Graph()
	counter = 0
	for tweet in tweets_array:
		counter += 1
		# Go through all hashtags array and add nodes if they don't exist yet.
		# Then we will connect them if a tweet contains multiple hash tags.
	 	for hashtag in tweet['entities']['hashtags']:
	 		#http://stackoverflow.com/questions/3224268/python-unicode-encode-error	
	 		tag = hashtag['text'].encode('ascii', 'ignore').lower()
	 		if not g.has_node(tag):
	 			g.add_node(tag, {'weight':0})
	 		else:
	 			g.node[tag]['weight'] += 1    #The weight is the number of times tag occurs
	 	
	 	#At this point, all tags in this tweet are connected.
	 	for hashtag1 in tweet['entities']['hashtags']:
	 		tag1 = hashtag1['text'].encode('ascii', 'ignore').lower()
	 		for hashtag2 in tweet['entities']['hashtags']:
	 			tag2 = hashtag2['text'].encode('ascii', 'ignore').lower()
	 			#Double for loop, but not too bad, add a bunch of edges!
	 			if not g.has_edge(tag1, tag2):
	 				g.add_edge(tag1, tag2, {'weight':0})
	 			else:
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

retweets_graph = retweeted_graph(retweets)

pruned_graph = retweets_graph.copy()
for node in pruned_graph.nodes():
	if pruned_graph.node[node]['weight'] < 30:
		pruned_graph.remove_node(node)

f.write_network_gml(pruned_graph, 'retweets_hashtag_gt30_lower')

# nx.draw(retweets_graph)
# plt.show()
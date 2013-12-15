"""Jennings Anderson 2013
CSCI 5352: Final Project: Boulder Flooding

This module creates a nodes of all users and tweets, connecting them if
that user made that tweet.  Multiple users will share tweets if they share keywords."""

import bf_load as bf
import proj_funcs as f
import networkx as nx
import matplotlib.pyplot as plt
								# Syntax for what is returned, true/false
users = []
tags  = []
def create_user_tweet_graph(tweets):
	'''Return graph based on global query:
	Nodes: Users, Hashtags (Different types, colors)
	Edges: Users --> Hashtags if user had tweet containing hashtag'''
	counter=0
	graph = nx.Graph()
	for tweet in tweets:
		user = tweet['user']['id']
		hashtags = []
		for tag in tweet['entities']['hashtags']:
			hashtags.append(tag['text'].encode('ascii', 'ignore').lower())

		#Add Users
		if not graph.has_node(user):
			graph.add_node(user, {'label':tweet['user']['screen_name'], 'weight':1, 
				'type': 'user', 'color':'red', 'bipartite':0} )
			users.append(user)
		else:
			graph.node[user]['weight']+=1

		for tag in hashtags:
			# Add Hashtag nodes
			if not graph.has_node(tag):
				graph.add_node(tag, {'label':tag, 'weight':1, 'type':'hashtag', 
					'color':'blue','bipartite':1} )
				tags.append(tag)
			else:
				graph.node[tag]['weight']+=1


			#Add edges
			if not graph.has_edge(user, tag):
				graph.add_edge(user, tag, {'weight':1} )
			else:
				graph[user][tag]['weight']+=1
		
		counter+=1
		if counter%1000==0:
			print counter,

	degrees = graph.degree(weight='weight')				# Need to get the appropriate weights
	for node in degrees.keys():
		graph.node[node]['real_degree'] = degrees[node]
	print "done"
	return graph

################################# RUN TIME ######################################

if __name__ == '__main__':
	# Query
	tweets = bf.query_mongo_get_list(bf.all_tweets)
	graph = create_user_tweet_graph(tweets)

	print "making bipartite..."
	
	tags = nx.bipartite.weighted_projected_graph(graph, tags)

	f.write_network_gml(tags, 'hashtag-bipartite-graph')
	
	#trimmed_users = f.trim_graph(graph,'weight', 10000, key='type', value='hashtags')
	#print "trimmed", len(trimmed_users)

	#f.draw_network_plt(trimmed_users, scale=1)

	#print len(trimmed_users.nodes())

	#f.draw_network_plt(trimmed_users, scale=1)
	
	#for node in graph.nodes():
	#	if graph.node[node]['weight'] < 10:
	#		graph.remove_node(node)

	# print "Making full_hist graph"
	# full_hist = f.bin_it(graph.degree())
	# print len(full_hist)
	# f.draw_graph(full_hist, scale='log', name='Degree_All_Nodes', style='go', sort=True, reverse=True )

	# print "Making user_hist graph"
	# node_type = nx.get_node_attributes(graph, 'type')
	# user_hist = f.bin_it(graph.degree(), type="user", type_dict=node_type)
	# print len(user_hist)
	# f.draw_graph(user_hist, scale='log', name='Degree_Just_Users', style='ro', sort=True, reverse=True)

	#f.write_network_gml(graph, 'user_tweets_gt_10')
	#Good - that works!
	# print 'Making graph of ',len(graph.nodes()),'nodes and', len(graph.edges()), 'edges'
	# f.draw_graph(histogram, style='ro', scale='log')




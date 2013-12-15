"""This model creates nodes of all users and hashtags, connecting them if
user tweeted with specific hashtag."""

import bf_load as bf
import proj_funcs as f
import networkx as nx
import matplotlib.pyplot as plt

#Globals
users = []
tags  = []
def create_user_tweet_graph(tweets):
	"""Return graph based on global query:
	Nodes: Users, Hashtags (Different types, colors)
	Edges: Users --> Hashtags if user had tweet containing hashtag"""
	counter=0
	graph = nx.Graph()
	for tweet in tweets:
		user = tweet['user']['id']
		hashtags = []
		for tag in tweet['entities']['hashtags']:
			hashtags.append(tag['text'].encode('ascii', 'ignore').lower())

		# Add Users	
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

	degrees = graph.degree(weight='weight')  # Need to get the appropriate weights
	for node in degrees.keys():
		graph.node[node]['real_degree'] = degrees[node]
	print "done"
	return graph

def calculate_lorenz_curve(graph, type, steps=100):
	"""Calculate the Lorenz curve graph based on the weight of the nodes."""
	vertices = {}
	total_weight = 0.0
	for node in graph.nodes():
		if graph.node[node]['type'] is type:
			vertices[node] = graph.node[node]['weight']
			total_weight  += graph.node[node]['weight']
	
	print 'Total Weight:', total_weight

	step_size = len(vertices.keys()) / steps
	# Now sort vertices by their weights:
	sorted_vertex_keys = sorted(vertices, key=vertices.get, reverse=True)
  	
  	y = [0]*steps
  	y_index = 0
  	cum_sum = 0.0
	for i in range(0, len(sorted_vertex_keys)):
		cum_sum += (vertices[sorted_vertex_keys[i]] / total_weight)
  		y[y_index] = cum_sum

  		if i % step_size == 0 and y_index<len(y)-1:
  			y_index += 1
  	
  	x=[]
  	x_sum=0.0
  	for i in range(0, steps):
  		x_sum += (float(step_size)/len(vertices.keys()))
  		x.append(x_sum)

  	return [x,y]

def investigate_top_tweets(graph):
	trimmed_graph = f.trim_graph(graph, 'weight', 50000, key='type', value='hashtags')
	trimmed_graph = f.trim_graph(trimmed_graph, 'weight', 500, key='type', value='user')
	degrees = trimmed_graph.degree()
	for node in degrees.keys():
		if degrees[node] < 1:
			trimmed_graph.remove_node(node)
	
	print len(trimmed_graph.nodes())

	#Normalize the weights for better drawing, now that it's trimmed:
	total_weights={'user':0, 'hashtag':1}
	for node in trimmed_graph.nodes():
		total_weights[trimmed_graph.node[node]['type']]+=trimmed_graph.node[node]['weight']
	for node in trimmed_graph.nodes():
		type=trimmed_graph.node[node]['type']
		total = float(total_weights[type])
		trimmed_graph.node[node]['normalized_weight'] = trimmed_graph.node[node]['weight'] / total
		if type is 'user':
			trimmed_graph.node[node]['normalized_weight'] *= 10000 #Scale for viewing
		else:
			trimmed_graph.node[node]['normalized_weight'] *= 1000

	f.write_network_gml(trimmed_graph, 'trimmed-user-tags-hi_threshold')
	
################################# RUN TIME ######################################

if __name__ == '__main__':
	#tweets = bf.query_mongo_get_list(bf.not_retweets)
	#graph = create_user_tweet_graph(tweets)

	"""Calculate the Lorenz Curves for Users & Hashtags"""
	#lorenz_hashtags = calculate_lorenz_curve(graph, 'hashtag', steps=100)
	#lorenz_users = calculate_lorenz_curve(graph, 'user', steps=100)
	#plt.plot(lorenz_hashtags[0],lorenz_hashtags[1], label="Hashtags")
	#plt.plot(lorenz_users[0], lorenz_users[1], label="Users")
	#f.draw_graph(plot=plt, title='Lorenz Curves for Users & Hashtags',
	# 	y_label='Percent of Tweets', x_label='Percent of Group', y_lim=[0,1], x_lim=[0,1])


	"""Investigating the top tweets"""
	#investigate_top_tweets(graph)

	"""One Mode Projections"""
	#tags = nx.bipartite.weighted_projected_graph(graph, tags)
	#bf.pickle_this(tags, 'one_mode_tags-noretweets')
	#users = nx.bipartite.weighted_projected_graph(graph, users)
	#bf.pickle_this(users, 'one_mode_users-noretweets')
	tags = bf.unpickle_this('one_mode_tags-noretweets')
	#users = bf.unpickle_this('one_mode_users-noretweets')

	print len(tags.nodes())
	#f.write_network_gml(tags, 'hashtag-bipartite-graph')
	
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




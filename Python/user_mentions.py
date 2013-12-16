"""Jennings Anderson 2013
CSCI 5352: Final Project: Boulder Flooding

This module handles the user mentions graph where users tag other users in
the actual tweet."""

import bf_load as bf
import proj_funcs as f
import networkx as nx
import matplotlib.pyplot as plt
import datetime

def user_mentions_graph(tweets_array):
	'''Creates User Mentions Graph:
		Nodes: Users
		Edges: Exist if user mentions user in tweet, weight = frequency'''
	g = nx.DiGraph()				#Make it a directed graph
	counter = 0
	user_names = {}
	for tweet in tweets_array:
		counter += 1
	 	this_user = int(tweet['user']['id'])

	 	# Handle multiple user names - will see if it is important to do so.
	 	if user_names.has_key(this_user) and not tweet['user']['screen_name'].encode('ascii', 'ignore') in user_names[this_user]:
	 		#http://stackoverflow.com/questions/3224268/python-unicode-encode-error		
	 		user_names[this_user].append(tweet['user']['screen_name'].encode('ascii', 'ignore'))
	 	else:
	 		user_names[this_user] = [tweet['user']['screen_name'].encode('ascii', 'ignore')]
	 	
	 	#Iterate through all of the mentioned users in a tweet
	 	mentions = tweet['entities']['user_mentions']
	 	for mentioned in mentions:
	 		mentioned_user = int(mentioned['id'])
			if user_names.has_key(mentioned_user) and not mentioned['screen_name'].encode('ascii', 'ignore') in user_names[mentioned_user]:
	 			user_names[mentioned_user].append(mentioned['screen_name'].encode('ascii', 'ignore'))
	 		else:
	 			user_names[mentioned_user] = [mentioned['screen_name'].encode('ascii', 'ignore')]
			
	 		if not g.has_edge(this_user, mentioned_user):
	 			g.add_edge(this_user, mentioned_user, weight=1)
	 		else:
	 			g[this_user][mentioned_user]['weight']+=1
	 	
	 	if counter % 1000 == 0:			# For status update, can take a while
	 		print counter,

	in_degree = g.in_degree(weight='weight')
	out_degree = g.out_degree(weight='weight')
	for node in g.nodes():
		g.node[node]['label'] = str(user_names[node]).strip('[\'\]')
		g.node[node]['in_degree'] = in_degree[node]
		g.node[node]['out_degree'] = out_degree[node]
		g.node[node]['degree'] = in_degree[node]+out_degree[node]
	
	print "----DONE----"
	return g

def plot_degree_vs_reciprocity():
	x,y,labels = f.print_top_reciprocated_nodes(large_component, count=10, return_graph=True)
	fig, ax = plt.subplots()
	ax.scatter(x, y)
	for i, txt in enumerate(labels):
		ax.annotate(txt, (x[i], y[i]), rotation=15,va='bottom')
	plt.title('Out Degree vs. Reciprocity')
 	plt.ylabel("Reciprocity per Node")
 	plt.xlabel("Out Degree")
	plt.show()

def print_top_betweenness(component, size=10):
	bc = nx.betweenness_centrality(component, weight='weight', normalized=True)
	for node in sorted(bc, key=bc.get, reverse=True)[0:size]:
		query = {'spec': {'user.id': int(node) }, 'fields':{'_id':0,'user.screen_name': 1} }
		this_data = bf.query_mongo_get_list(query, limit=1)
		print this_data['user']['screen_name'],'&', "{0:.4f}".format(bc[node]), '\\\\'
	return bc

if __name__ == '__main__':
	"""First, get only geo_tagged_tweets"""
	geo_tagged_user_mentions = bf.query_mongo_get_list(bf.only_geo_tagged)
	print "Geo_Tagged found:", len(geo_tagged_user_mentions), "Making Graph..."
	umg_geo = user_mentions_graph(geo_tagged_user_mentions)
	print 'Users',len(umg_geo.nodes())
	# connected_components = nx.weakly_connected_component_subgraphs(umg_geo)
	# print "Number of Connected Components:", len(connected_components)
	# for subgraph in connected_components[0:5]:
	# 	print "Component has", len(subgraph.nodes())
	# #f.draw_network_plt(connected_components[1])
	print '\nreciprocity, weighted:',   f.get_graph_reciprocity(umg_geo)
	print 'reciprocity, unweighted:', f.get_graph_reciprocity(umg_geo, weighted=False)
	#print f.reciprocity_by_degree(umg_geo, 'in')

	print "self loops:"
	f.print_top_self_loops(umg_geo, size=10)


	"""geo_tagged_plus: All users who interact with geo_tagged users"""
	geo_tagged_plus = bf.get_all_users_who_interact_with(umg_geo.nodes())
	print "Geo_Tagged_Plus found:", len(geo_tagged_plus)
	umg_geo_plus = user_mentions_graph(geo_tagged_plus)
	print 'Users:',len(umg_geo_plus.nodes())

	f.print_top_self_loops(umg_geo_plus, size=10)
	#print '\nreciprocity, weighted:',   f.get_graph_reciprocity(umg_geo_plus)
	#print 'reciprocity, unweighted:', f.get_graph_reciprocity(umg_geo_plus, weighted=False)

	#f.print_top_reciprocated_nodes(umg_geo_plus, count=20, reverse=True, return_graph=False)
	#f.print_betweenness_centrality(umg_geo_plus, amount=10)


	"""The entire network without retweets"""
	#user_mentions_no_retweets = bf.query_mongo_get_list(bf.not_retweets)
	#print "Tweets found:", len(user_mentions_all), "Making Graph..."
	#umg_all = user_mentions_graph(user_mentions_all)

	
	#to_draw = f.trim_graph(umg_all,'degree',100)
	#print len(to_draw.nodes())


	# print "Number of components:",
	# components = nx.weakly_connected_component_subgraphs(umg_geo_plus)
	# print len(components)
	# large_component = components[1]
	# print "Nodes in Giant Component: ",len(large_component.nodes())

	# print '\nTop 10 Self loops in giant component:'
	# f.print_top_self_loops(large_component, size=10)

	# trimmed = f.trim_graph(large_component, 'degree', 100)
	# print len(trimmed.nodes())

	# f.draw_network_plt(trimmed, size='degree', scale=1)
	
	#undirected_umg = umg_plus.to_undirected()
	
	#f.print_top_reciprocated_nodes(large_component, count=10)
	
	#f.write_network_gml(umg, 'geo-tagged-user-mentiones-graph')
	#bc = nx.betweenness_centrality(umg, normalized=True)
	#draw_graph(bc, sort=True, style="ro" )

	# This is not that interesting, but it's here:
	#dc = nx.degree_centrality(large_component)
	#f.draw_graph(dc, sort=True, style="r-", reverse=True, y_axis="Degree Centrality", x_axis="Number of Nodes")
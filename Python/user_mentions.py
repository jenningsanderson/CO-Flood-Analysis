"""Jennings Anderson 2013
CSCI 5352: Final Project: Boulder Flooding

This module handles the user mentions graph where users tag other users in
the actual tweet."""

import bf_load as bf
import proj_funcs as f
import networkx as nx
import matplotlib.pyplot as plt
import datetime

in_array_users_query = []
nodes_array = []

#start = datetime.datetime(2013, 9, 13, 5, 00, 00)
#end = datetime.datetime(2013, 9, 13, 6, 00, 00)

# query = {	'spec':	{'created_at': {'$gt': start, '$lt': end } },
# 			'fields':{	'_id'		:0, 
# 						'id'		:1, 
# 						'user.screen_name': 1, 
# 						'text'		:1,
# 						'user.id'	:1, 
# 						'entities.user_mentions':1 }	}

query = {	'spec': {'geo': {'$ne': None }},	#Only geolocated tweets?
			'fields':{	'_id':0, 'id':1, 'user.screen_name': 1, 'text':1,
						'user.id':1, 'entities.user_mentions':1}
		}

#Query for getting tweets that mention specific users.
query2 = {	'spec': {'$or': [{'user.screen_name':{'$in':in_array_users_query}}, {'entities.user_mentions.screen_name':{'$in':in_array_users_query}}]},	#Only geolocated tweets?
			'fields':{	'_id':0, 'id':1, 'user.screen_name': 1, 'text':1,
						'user.id':1, 'entities.user_mentions':1}
		}

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
	
	print "----DONE----"	
	return g

def show_component_histogram(components, bins=None, debug=False):
	hist_list = []
	for i in components:
		hist_list.append(len(i))
	if debug:
		print hist_list
	if bins:
		plt.hist(hist_list, bins=bins, histtype='stepfilled')
	else:
		plt.hist(hist_list, histtype='stepfilled')
	plt.title("Size of Components Histogram - Geo-Tagged")
	plt.xlabel("Nodes in Component")
	plt.xscale('log')
	plt.ylabel("Number of Components")
	plt.show()

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
		in_array_users_query.append(this_data['user']['screen_name'])
		nodes_array.append(node)
	return bc

def find_self_loops(graph):
	self_loop_weights = {}
	for self_loop in graph.selfloop_edges():
		weight = graph[self_loop[0]][self_loop[1]]['weight']
		if not self_loop_weights.has_key(weight):
			self_loop_weights[weight] = [self_loop[0]]
		else:
			self_loop_weights[weight].append(self_loop[0])

	weights_array = self_loop_weights.keys()
	weights_array.sort()
	weights_array.reverse()
	for weight in weights_array[0:15]:
		print weight,"&",
		if len(self_loop_weights[weight])>1:
			comma=","
		else:
			comma=""
		for j in self_loop_weights[weight]:
			query = {'spec': {'user.id': int(j) }, 'fields':{'_id':0, 'user.screen_name': 1, 'text':1} }
			this_data = bf.query_mongo_get_list(query, limit=1)
			print this_data['user']['screen_name'], comma, 
		print "\\\\"

if __name__ == '__main__':
	
	user_mentions = bf.query_mongo_get_list(query)	#Query defined above
	print "Tweets found:", len(user_mentions), "Making Graph..."	
	
	umg = user_mentions_graph(user_mentions)

	print "Number of components:",
	components = nx.weakly_connected_component_subgraphs(umg)
	print len(components)
	large_component = components[0]
	print "Nodes in Giant Component: ",len(large_component.nodes())

	print f.get_graph_reciprocity(large_component)
	print f.get_graph_reciprocity(large_component, weighted=False)

	undirected_umg = umg.to_undirected()

	print_top_betweenness(undirected_umg, 10)
	#f.draw_graph(print_top_betweenness(undirected_umg, 10), 
		# sort=True, reverse=True, style='ro', scale='log', 
		# title="Betweenness Centrality of Geo-Tagged User Mentions", 
		# x_axis="Nodes", y_axis="Betweenness Centrality")

	#Now we've identified the users that we care about as in_array_query
	print "Using above list to create new graph, calling all users that tweeted at those users"
	user_mentions2 = bf.query_mongo_get_list(query2)	#Query defined above
	print "Tweets found:", len(user_mentions2), "Making Graph..."
	
	umg2 = user_mentions_graph(user_mentions2)

	print "Number of components:",
	components = nx.weakly_connected_component_subgraphs(umg2)
	print len(components)
	large_component = components[0]
	print "Nodes in Giant Component: ",len(large_component.nodes())

	#print f.get_graph_reciprocity(large_component)
	#print f.get_graph_reciprocity(large_component, weighted=False)
	for i in range(0, len(nodes_array)):
		print in_array_users_query[i], "&", "{0:.4f}".format( f.get_reciprocity_of_node(umg2, nodes_array[i]) ), "\\\\"
	

	#f.write_network_gml(umg2, 'users-mentioning-geo-tagged-users-digraph')

	#For Geo-tagged:
	#show_component_histogram(components, bins=(0,1,2,3,4,5,6,7,10,13,500,600))
	
	#f.print_top_reciprocated_nodes(large_component, count=10)
	
	#f.write_network_gml(umg, 'geo-tagged-user-mentiones-graph')
	# bc = nx.betweenness_centrality(umg, normalized=True)
	#draw_graph(bc, sort=True, style="ro" )


	# This is not that interesting, but it's here:
	#dc = nx.degree_centrality(large_component)
	#f.draw_graph(dc, sort=True, style="r-", reverse=True, y_axis="Degree Centrality", x_axis="Number of Nodes")



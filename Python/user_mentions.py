"""Jennings Anderson 2013
CSCI 5352: Final Project: Boulder Flooding

This module handles the user mentions graph and does computations for that."""
import bf_load as bf
import proj_funcs as f
import networkx as nx
import matplotlib.pyplot as plt
import datetime

############################# Top Tweet Hours
# 2013-09-13 00:00:00 5548
# 2013-09-12 12:00:00 4961
# 2013-09-12 23:00:00 4728
# 2013-09-12 22:00:00 4345
# 2013-09-12 10:00:00 4071
# 2013-09-12 13:00:00 3976
# 2013-09-12 21:00:00 3806
# 2013-09-12 20:00:00 3583
# 2013-09-12 11:00:00 3517
# 2013-09-13 10:00:00 3371
# 2013-09-12 09:00:00 3351
# 2013-09-13 01:00:00 3343
# 2013-09-12 14:00:00 3194
# 2013-09-13 11:00:00 3142
# 2013-09-12 16:00:00 3052
# 2013-09-12 17:00:00 3039

start = datetime.datetime(2013, 9, 12, 17, 00, 00)
end = datetime.datetime(2013, 9, 12, 18, 00, 00)

# query = {	'spec':	{'created_at': {'$gt': start, '$lt': end } },
# 			'fields':{	'_id'		:0, 
# 						'id'		:1, 
# 						'user.screen_name': 1, 
# 						'text'		:1,
# 						'user.id'	:1, 
# 						'entities.user_mentions':1 }	}

query = {	'spec':	{}, #{'geo': {'$ne': None }},	#Only geolocated tweets?
			'fields':{	'_id':0, 'id':1, 'user.screen_name': 1, 'text':1,
						'user.id':1, 'entities.user_mentions':1}
		}

def user_mentions_graph(tweets_array):	# Required fields: 'user.id', 'entities.user_mentions'
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
	 	for mentioned in mentions:								# Iterate through each user name in tweet
	 		
	 		mentioned_user = int(mentioned['id'])
			if user_names.has_key(mentioned_user) and not mentioned['screen_name'].encode('ascii', 'ignore') in user_names[mentioned_user]:
	 			user_names[mentioned_user].append(mentioned['screen_name'].encode('ascii', 'ignore'))
	 		else:
	 			user_names[mentioned_user] = [mentioned['screen_name'].encode('ascii', 'ignore')]
			
	 		if not g.has_edge(this_user, mentioned_user):
	 			g.add_edge(this_user, mentioned_user, weight=1)
	 		else:
	 			g[this_user][mentioned_user]['weight']+=1
	 	
	 	if counter % 1000 == 0:							# For status update, can take a while
	 		print counter,

	in_degree = g.in_degree(weight='weight')
	out_degree = g.out_degree(weight='weight')
	for node in g.nodes():
		g.node[node]['label'] = str(user_names[node]).strip('[\'\]')
		g.node[node]['in_degree'] = in_degree[node]
		g.node[node]['out_degree'] = out_degree[node]
	
	print "----DONE----"	
	return g

if __name__ == '__main__':
	print 'Start:', start
	print 'End:', end
	
	user_mentions = bf.query_mongo_get_list(query)
	print len(user_mentions)
	
	umg = user_mentions_graph(user_mentions)

	#large_component = nx.weakly_connected_component_subgraphs(umg)[0]
	large_component = umg


	for node in umg.nodes()[0:10]:
		if len(umg.node[node]['label'])>1:
			print umg.node[node]['label']
	#Compute the betweenness centrality of the User-mentions graph (For all the users)
	#bc = nx.betweenness_centrality(large_component)
	#print len(bc.values())
	#print 'zeroes', bc.values().count(0.0)

	#f.draw_network_plt(large_component, scale=1)

	# for node in sorted(bc, key=bc.get, reverse=True)[0:10]:
	# 	query = {'spec': {'user.id': int(node) }, 'fields':{'_id':0, 'user.screen_name': 1} }
	# 	this_data = bf.query_mongo_get_list(query, limit=1)
	# 	print this_data['user']['screen_name'],'&', "{0:.4f}".format(bc[node]), '\\\\'

	# #f.draw_graph(bc, sort=True, reverse=True, style='ro', scale='log')

	# for node in large_component.nodes():
	# 	large_component.node[node]['weight'] = int(10000000*bc[node])
	# 	large_component.node[node]['label'] = user_names[node]

	#f.write_network_gml(large_component, 'testing_degrees')


	# self_loop_weights = {}
	# for self_loop in umg.selfloop_edges():
	# 	weight = umg[self_loop[0]][self_loop[1]]['weight']
	# 	if not self_loop_weights.has_key(weight):
	# 		self_loop_weights[weight] = [self_loop[0]]
	# 	else:
	# 		self_loop_weights[weight].append(self_loop[0])

	# weights_array = self_loop_weights.keys()
	# weights_array.sort()
	# weights_array.reverse()
	# for weight in weights_array[0:15]:
	# 	print weight,"&",
	# 	if len(self_loop_weights[weight])>1:
	# 		comma=","
	# 	else:
	# 		comma=""
	# 	for j in self_loop_weights[weight]:
	# 		query = {'spec': {'user.id': int(j) }, 'fields':{'_id':0, 'user.screen_name': 1, 'text':1} }
	# 		this_data = bf.query_mongo_get_list(query, limit=1)
	# 		print this_data['user']['screen_name'], comma, 
	# 	print "\\\\"


	# degrees = nx.degree(umg)

	# pruned_umg = umg.copy()

	# for node in pruned_umg.nodes():
	# 	if degrees[node] < 500:
	# 		pruned_umg.remove_node(node)

	# print len(pruned_umg.nodes())
	# avg_reciprocity = 0.0
	# counter = 0
	# for node in umg.nodes():
	# 	counter+=1
	# 	avg_reciprocity += f.get_reciprocity_of_node(umg, node)
	# 	if counter % 1000==0:
	# 		print counter,

	# print avg_reciprocity / (len(umg.nodes()))

	#components = nx.weakly_connected_component_subgraphs(umg)

	# hist_list = []
	# for i in components:
	# 	hist_list.append(len(i))

	# print hist_list


	# plt.hist(hist_list, bins=(0,1,2,3,4,5,6,7,10,13,500,600), histtype='stepfilled')
	# plt.title("Size of Component Histogram")
	# plt.xlabel("Size of Component")
	# plt.xscale('log')
	# plt.ylabel("Number of Components")
	# plt.show()

	# counter=0
	# for i in components[0:3]:
	# 	print len(i.nodes())
	# 	counter+=1
	# 	f.write_network_gml(i, 'umg_subgraph_'+str(counter))
	 

	#Important - find components:

	#f.write_network_gml(pruned_umg, 'umg_pruned')

	#reciprocity_by_degree(umg, 'out', 15)
	#What does it look like?
	#nx.draw(umg)
	#plt.show()

	# bc = nx.betweenness_centrality(umg, normalized=True)
	# dc = nx.degree_centrality(umg)
	# print len((umg.nodes()))
	# draw_graph(bc, sort=True, style="ro" )
	# draw_graph(dc, sort=True, style="go", y_scale='log')



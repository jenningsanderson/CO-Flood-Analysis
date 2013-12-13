"""Jennings Anderson 2013
CSCI 5352: Final Project: Boulder Flooding

This module gives follower_assortativity by user_mentions."""

import bf_load as bf
import proj_funcs as f
import networkx as nx
import matplotlib.pyplot as plt
import datetime

#start = datetime.datetime(2013, 9, 12, 17, 00, 00)
#end = datetime.datetime(2013, 9, 12, 18, 00, 00)

#print 'Start:', start
#print 'End:', end

# query = {	'spec':	{'created_at': 
# {'$gt': start, '$lt': end } },
# 			'fields':{	'_id':0, 'id':1, 'user.screen_name': 1, 'text':1,
# 						'user.id':1, 'entities.user_mentions':1}
#		}

query = {	'spec':	{}, #{'geo': {'$ne': None }},	#Only geolocated tweets?
 			'fields':{	'_id':0, 'id':1, 'user.screen_name': 1, 'text':1,
 						'user.id':1, 'entities.user_mentions':1, 'user.followers_count':1}
 		}

user_mentions = bf.query_mongo_get_list(query)
#print len(user_mentions)

# user_names = {}
# user_followers = {}
def user_mentions_graph(tweets_array):	# Required fields: 'user.id', 'entities.user_mentions'
	g = nx.DiGraph()				#Make it a directed graph
	counter = 0
	user_tweet_counts = {}	
	for tweet in tweets_array:
		counter += 1
	 	this_user = int(tweet['user']['id'])
	 	user_names[this_user] = tweet['user']['screen_name']
	 	
	 	if not user_followers.has_key(this_user):
	 		user_followers[this_user] = [tweet['user']['followers_count']]
	 	else:
	 		if not tweet['user']['followers_count'] in user_followers[this_user]:
	 			user_followers[this_user].append(tweet['user']['followers_count'])
	 		
	 	mentions = tweet['entities']['user_mentions']
	 	
	 	if user_tweet_counts.has_key(this_user):		# Count the tweets per user
	 		user_tweet_counts[this_user] += 1
	 	else:
	 		user_tweet_counts[this_user] = 1
	 	
	 	for j in mentions:								# Iterate through each user name in tweet
	 		mention_user = int(j['id'])
			user_names[mention_user] = j['screen_name']
			#http://stackoverflow.com/questions/3224268/python-unicode-encode-error					
	 		if not g.has_edge(this_user, mention_user):
	 			g.add_edge(this_user, mention_user, {'weight':0})
	 		else:
	 			g[this_user][mention_user]['weight']+=1
	 	if counter % 1000 == 0:							# For status update, can take a while
	 		print counter,
	print "----DONE----"	
	return [g, user_tweet_counts]

if __name__ == '__main__':
		
	umg, user_tweet_counts = user_mentions_graph(user_mentions)

	#f.draw_graph(bc, sort=True, reverse=True, style='ro', scale='log')

	for node in umg.nodes():
		umg.node[node]['label'] = user_names[node]
		if user_followers.has_key(node):
			diff = max(user_followers[node])-min(user_followers[node])
			avg_follower_count=int(f.get_avg(user_followers[node]))
			if diff < 500: #Set higher to prune the graph
				umg.remove_node(node)
			else:
				umg.node[node]['follower_diff'] = diff
				umg.node[node]['follower_avg'] = avg_follower_count
		else:
			umg.remove_node(node)

	#print nx.numeric_assortativity_coefficient(umg, 'follower_avg')


		#if diff > 5:
		#	print user_names[key], diff

		#umg.node[key]['followers_count'] = user_followers[key]

	f.write_network_gml(umg, 'follower_diff_gt500')

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

	def reciprocity_by_degree(graph, degree_type='in', size=20):
		if degree_type is 'in':
			degrees = graph.in_degree()
		if degree_type is 'out':
			degrees = graph.out_degree()
		avg_reciprocity = 0.0
		for w in sorted(degrees, key=degrees.get, reverse=True)[0:size]:
			print degrees[w], "&",
			query = {'spec': {'user.id': int(w) }, 'fields':{'_id':0, 'user.screen_name': 1, 'text':1} }
			this_data = bf.query_mongo_get_list(query, limit=1)
			reciprocity = f.get_reciprocity_of_node(umg, int(w))
			print this_data['user']['screen_name'], "\\\\"#,"&", "{0:.4f}".format(reciprocity),"\\\\"
			avg_reciprocity+=reciprocity
		print avg_reciprocity/size

	#reciprocity_by_degree(umg, 'out', 15)
	#What does it look like?
	#nx.draw(umg)
	#plt.show()

	# bc = nx.betweenness_centrality(umg, normalized=True)
	# dc = nx.degree_centrality(umg)
	# print len((umg.nodes()))
	# draw_graph(bc, sort=True, style="ro" )
	# draw_graph(dc, sort=True, style="go", y_scale='log')


	#large_component = nx.weakly_connected_component_subgraphs(umg)[0]

	#Compute the betweenness centrality of the User-mentions graph (For all the users)
	# bc = nx.betweenness_centrality(large_component)
	# print len(bc.values())
	# print 'zeroes', bc.values().count(0.0)

	# for node in sorted(bc, key=bc.get, reverse=True)[0:10]:
	# 	query = {'spec': {'user.id': int(node) }, 'fields':{'_id':0, 'user.screen_name': 1} }
	# 	this_data = bf.query_mongo_get_list(query, limit=1)
	# 	print this_data['user']['screen_name'],'&', "{0:.4f}".format(bc[node]), '\\\\'
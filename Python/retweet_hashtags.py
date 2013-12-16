"""This module builds hashtag networks based on retweet frequency.
Hashtags are nodes and edges exist between them if they appear in the same tweet.
This is similar to a word cloud, but shows relation between tweets.

The hope is that by identifying clusters, SPAM keywords can be easily identified."""

import bf_load as bf
import proj_funcs as f
import networkx as nx
import matplotlib.pyplot as plt

def retweeted_graph(tweets_array):
	"""Returns retweeted graph from tweets array returned from mongoDB"""
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
	 			g.node[tag]['weight'] += 1  # Weight is # times hashtag occurs

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
	 	
	 	if counter % 1000 == 0:		# For status update, can take a while
	 		print counter,
	#Apply the appropriate degree to each hashtag...
	degrees = g.degree(weight='weight')
	for node in degrees.keys():
		g.node[node]['real_degree']=degrees[node]
		g.node[node]['label']=node
	
	print "----DONE----"
	return g

def make_triangle_cc_plot(graph, threshold=100, show_labels=False):
	"""Create a Plot of #Triangles vs. Clustering Coefficient for each node.
	
	|  Function Options: 
	|  Threshold: Maximum # triangles per node to be included in plot.
	|  show_labels (defaults to false): Tells Matplotlib to show labels or not"""
	tris =  nx.triangles(graph)
	clustering = nx.clustering(graph, weight='weight')
	cc_to_graph = []
	tris_to_graph = []
	labels = []
	fig, ax = plt.subplots()
	print  "{:15s}".format("Node"), "Tris", "CC"
	for i in tris.keys():
		if tris[i] < threshold:
			print "{:15s}".format(i), "&",
			print "{:3d}".format(tris[i]), "&",
			print "{0:.4f}".format(clustering[i]),
			print "\\\\"
			cc_to_graph.append(clustering[i])
			tris_to_graph.append(tris[i])
			labels.append(i)

	ax.scatter(cc_to_graph, tris_to_graph)
	
	if show_labels:
		for i, txt in enumerate(labels):
			ax.annotate(txt, (cc_to_graph[i], tris_to_graph[i]), rotation=5)

	plt.plot([-1,1],[0,0],'k-')  # Put some Axis on the graph
	plt.plot([0,0],[0,1000], 'k-') 

	#plt.plot([-.01,1],[],'r-')

	plt.title('Number of Triangles vs. Clustering Coefficient')
 	plt.ylabel("Triangles")
 	plt.xlabel("Clustering Coefficient")
 	plt.xlim([0,.06])
 	plt.ylim([0,60])
	
	return plt

############################## RUNTIME #######################################
if __name__ == '__main__':
	# Get all retweets
	retweets = bf.query_mongo_get_list(bf.retweets)
	print "Number of Retweets: ", len(retweets)		
	retweets_graph = retweeted_graph(retweets)
	print "Nodes: ", len(retweets_graph.nodes()), "Edges: ", len(retweets_graph.edges())
	
	# Trim nodes to greater than 500
	trimmed_retweets = f.trim_graph(retweets_graph,'weight', 500)
	print "Trimmed to 500:",len(trimmed_retweets.nodes())
	#f.write_network_gml(trimmed_retweets,'retweeted_hashtags_gt_500')
	
	# Triangles Vs. Clustering Coefficient
	make_triangle_cc_plot(trimmed_retweets, show_labels=True, threshold=60).show()

	# Centralities:
	#f.print_betweenness_centrality(trimmed_retweets)
	
	# f.write_network_gml(pruned_graph, 'retweets_hashtag_gt800_real_degree')

	#f.draw_network_plt(pruned_graph, scale=(.1))	#For quick visualization

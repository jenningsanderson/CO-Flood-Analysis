"""Jennings Anderson 2013
CSCI 5352: Final Project: Boulder Flooding

This module holds functions used in multiple parts of the analysis project."""
import matplotlib.pyplot as plt
import networkx as nx
import datetime

def draw_graph(dict, x_axis=False, y_axis=False, title=False, x_scale=False, y_scale=False, style=False, sort=False, scale=False, name=False, reverse=False, y_lim=False):
	"""Creates a matploblib graph from a dictionary.  
	Takes arguments for titles, axis, and scales"""
 	if not y_axis:  y_axis = 'Y Axis';
 	if not x_axis:  x_axis = 'X Axis';
 	if not title:   title  = 'Title';
 	if not x_scale: x_scale= 'linear';
 	if not y_scale: y_scale= 'linear'; 
 	if not style:   style  = 'g-';
 	if scale:  y_scale=scale;
 	if scale:  x_scale=scale;

 	y_vals = []
 	for key in dict.keys():
 		y_vals.append(dict[key])

 	if sort:
 		y_vals.sort()
 	if reverse:
 		y_vals.reverse()

 	plt.plot(range(0, len(y_vals)), y_vals, style)
 	plt.title(title)
 	plt.yscale(y_scale)
 	plt.xscale(x_scale)
 	plt.ylabel(y_axis)
 	plt.xlabel(x_axis)
 	if y_lim:
 		plt.ylim(y_lim)

 	if not name:
 		plt.show()
 	else:
 		plt.savefig('../Images/Graphs/'+str(name)+'.png')
 	plt.clf()

def bin_it(dict, histogram=True, type=False, type_dict=False):
	"""Converts data to counts for easy histogram-like viewing"""
	counts = {}
	hist   = {}
	for key in dict.keys():					#Typically, keys are nodes; but it works for all...
		if type and type_dict[key]==type:
			if counts.has_key(dict[key]):
				counts[dict[key]].append(key)
				hist[dict[key]] += 1
			else:
				counts[dict[key]] = [key]
				hist[dict[key]] = 1
		elif not type:
			if counts.has_key(dict[key]):
				counts[dict[key]].append(key)
				hist[dict[key]] += 1
			else:
				counts[dict[key]] = [key]
				hist[dict[key]] = 1
	if histogram:
		return hist
	else:
		return counts

def draw_network_plt(graph, name=False, scale=100):
	"""Will create a networkx matplotlib graph.
	Options: If name is specified, will save with name, otherwise will show plot"""
	colors	 		= False
	sizes  			= False
	scaled_sizes 	= False
	if 'color' in graph.nodes(data=True)[0][1].keys():
		colors = nx.get_node_attributes(graph, 'color').values()
	if 'weight' in graph.nodes(data=True)[0][1].keys():
		sizes = nx.get_node_attributes(graph, 'weight').values()
		scaled_sizes = [x * scale for x in sizes] 
	if colors and scaled_sizes:
		nx.draw(graph, node_size=scaled_sizes, node_color=colors)
	elif colors and not scaled_sizes:
		nx.draw(graph, node_color=colors)
	elif scaled_sizes and not colors:
		nx.draw(graph, node_size=scaled_sizes)
	else:
		nx.draw(graph)
	if not name:
		plt.show()
	else:
		plt.savefig('../Images/'+str(name)+'.png') # TODO: Make it save this graph to a directory.
	plt.clf()

def write_network_gml(graph, name):
	"""Creates .gml file from networkx graph object passed in.
	Must include a filename.  This can then be easily imported into Gephi"""
	print "Writing Network to GML...",
	nx.write_gml(graph, '../Gephi/'+str(name)+'.gml')
	print "done"

def roundTime(dt=None, roundTo=60):
   """Round a datetime object to any time laps in seconds
   dt : datetime.datetime object, default now.
   roundTo : Closest number of seconds to round to, default 1 minute.
   Author: Thierry Husson 2012 - Use it as you want but don't blame me.
   Source: http://stackoverflow.com/questions/3463930/how-to-round-the-
   		   minute-of-a-datetime-object-python/10854034#10854034"""
   if dt == None : dt = datetime.datetime.now()
   seconds = (dt - dt.min).seconds
   # // is a floor division, not a comment on following line:
   rounding = (seconds+roundTo/2) // roundTo * roundTo
   return dt + datetime.timedelta(0,rounding-seconds,-dt.microsecond)

def get_reciprocity_of_node(graph, node):
	"""Custom reciprocity function, must compare to function in networks text"""
	neighbor_iter = nx.all_neighbors(graph, node)
	reciprocated_links = 0.0
	unreciprocated_links = 0.0
	total_degree = 0
	for neighbor in neighbor_iter:
		total_degree += 1
		if graph.has_edge(node, neighbor) and graph.has_edge(neighbor, node):
			reciprocated_links+=.5 # (It will count this twice)
		else:
			unreciprocated_links+=1
	return (reciprocated_links) / (total_degree - reciprocated_links)

def get_graph_reciprocity(graph, weighted=True):
	"""Compute graph reciprocity: reciprocated links / total links"""
	edge_list = graph.edges(data=True)
	total_edges = len(edge_list) #Must account for the weight of the edges as well.
	reciprocated_links = 0.0
	new_list = []
	# for edge in edge_list:
	if weighted:
		for edge in edge_list:
			while edge[2]['weight'] > 0:
			 	new_list.append( (edge[0],edge[1]) )
			 	edge[2]['weight']-=1
		edge_list = new_list
		total_edges = len(new_list)
	
	elif (not weighted and edge_list[0][2] is not None):
		for edge in edge_list:
			 new_list.append( (edge[0],edge[1]) )
		edge_list = new_list
		total_edges = len(new_list)

	for edge in edge_list:
		if (edge[1],edge[0]) in edge_list:
			reciprocated_links+=2
			edge_list.remove( (edge[1], edge[0]) )
	return reciprocated_links / total_edges

def get_avg(list):
	"""Simply returns the average of a list"""
	avg = 0.0
	for i in list:
		avg+=i
	return avg/len(list)

def reciprocity_by_degree(graph, degree_type='in', size=20):
	"""Returns reciprocity (specified by in/out degree )
		**Need to compare to reciprocity formula in Networks Text.
		Formatted for LaTeX table output."""
	if degree_type is 'in':
		degrees = graph.in_degree()
	if degree_type is 'out':
		degrees = graph.out_degree()
	avg_reciprocity = 0.0
	for w in sorted(degrees, key=degrees.get, reverse=True)[0:size]:
		print degrees[w], "&",
		reciprocity = f.get_reciprocity_of_node(umg, int(w))
		print this_data['user']['screen_name'], "\\\\"#,"&", "{0:.4f}".format(reciprocity),"\\\\"
		avg_reciprocity+=reciprocity
	print avg_reciprocity/size

def print_betweenness_centrality(graph, amount=10):
	""" Prints the betweenness centrality for the top specificed # of nodes.
		Uses NetworkX's betweenness_centrality function.
		Depends on having weighted"""
	bc = nx.betweenness_centrality(graph, weight='weight')
	print "Top "+str(amount)+" Nodes by Betweenness Centrality:"
	for node in sorted(bc, key=bc.get, reverse=True)[0:amount]:
		print "{:15s}".format(graph.node[node]['label']), 
		print "{0:4f}".format(bc[node])

def print_top_reciprocated_nodes(graph, count):
	recips = {}
	recip_return = {}
	for node in graph.nodes():
		recips[node] = get_reciprocity_of_node(graph, node)
	for w in sorted(recips, key=recips.get, reverse=True)[0:count]:
		print graph.node[w]['label'], "&","{0:4f}".format(recips[w]), "\\\\"
	#return recip_return


if __name__ == '__main__':
	test_graph = nx.DiGraph()
	test_graph.add_edge(0,1,weight=2)
	test_graph.add_edge(1,2,weight=4)
	test_graph.add_edge(2,1,weight=4)
	test_graph.add_edge(2,0,weight=2)
	test_graph.add_edge(3,2,weight=2)
	test_graph.add_edge(3,0,weight=2)
	test_graph.add_edge(0,3,weight=2)

	print get_graph_reciprocity(test_graph)

	print_top_reciprocated_nodes(test_graph, 4)

	#nx.draw(test_graph)
	#plt.show()


"""This module holds various general functions for the project such as creating graphs.
"""
import matplotlib.pyplot as plt
import networkx as nx
import datetime

def ignore_KeyError(dict, key):
	try:
		if dict.has_key(key):
			return dict[key]
	except (KeyError):
		return False

def draw_graph(dict=False, x=False, y=False, **kwargs):
	"""Creates a matploblib graph from a dictionary.

	|  Will sort the dictionary if requested.
	|  If name argument is specified, it saves figure instead of showing it.
	|  Takes arguments for titles, axis, and scales.
	"""
	y_label = ignore_KeyError(kwargs, 'y_label') or 'Y Axis'
	x_label = ignore_KeyError(kwargs, 'x_label') or 'X Axis'
	title  	= ignore_KeyError(kwargs, 'title')   or 'Title'  #Ruby would be much easer...
	x_scale	= ignore_KeyError(kwargs, 'x_scale') or 'linear'
	y_scale	= ignore_KeyError(kwargs, 'y_scale') or 'linear'
	style 	= ignore_KeyError(kwargs, 'style') 	 or 'g-'
	scale 	= False or ignore_KeyError(kwargs, 'scale')
	y_lim 	= False or ignore_KeyError(kwargs, 'y_lim')
	name 	= False or ignore_KeyError(kwargs, 'name')
	sort 	= False or ignore_KeyError(kwargs, 'sort')
	reverse = False or ignore_KeyError(kwargs, 'reverse')

	if scale:
		y_scale = scale
		x_scale = scale
	
	y_vals = y or dict.values()
	x_vals = x or range(0, len(y_vals))
 
 	if sort:
 		y_vals.sort()
 	if reverse:
 		y_vals.reverse()

 	plt.plot(x_vals, y_vals, style)
 	
 	plt.title(title)
 	plt.yscale(y_scale)
 	plt.xscale(x_scale)
 	plt.ylabel(y_label)
 	plt.xlabel(x_label)
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

def draw_network_plt(graph, name=False, scale=100, size=False):
	"""Will create a networkx matplotlib graph.
	Options: If name is specified, will save with name, otherwise will show plot"""
	colors          = False
	scaled_sizes    = False
	labels          = {}
	for node in graph.nodes():
		labels[node] = graph.node[node]['label']
	if 'color' in graph.nodes(data=True)[0][1].keys():
		colors = nx.get_node_attributes(graph, 'color').values()
	if size:
		sizes = nx.get_node_attributes(graph, size).values()
		scaled_sizes = [x * scale for x in sizes]
	if colors and scaled_sizes:
		nx.draw(graph, node_size=scaled_sizes, node_color=colors, labels=labels)
	elif colors and not scaled_sizes:
		nx.draw(graph, node_color=colors, labels=labels)
	elif scaled_sizes and not colors:
		nx.draw(graph, node_size=scaled_sizes, labels=labels)
	else:
		nx.draw(graph, labels=labels)
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
	
	else:
		for edge in edge_list:
			 new_list.append( (edge[0],edge[1]) )
		edge_list = new_list
		total_edges = len(new_list)

	for edge in edge_list:
		if (edge[1],edge[0]) in edge_list:
			reciprocated_links+=2
			edge_list.remove( (edge[1], edge[0]) )
	if total_edges != 0:
		return reciprocated_links / total_edges
	else:
		return 0

def get_avg(list):
	"""Simply returns the average of a list"""
	avg = 0.0
	for i in list:
		avg+=i
	return avg/len(list)

def trim_graph(graph, criteria, limit, key=False, value=False):
	trim_graph = graph.copy()
	if key and value:
		node_types = nx.get_node_attributes(trim_graph, key)
	for node in trim_graph.nodes():
		if key and value:
			if node_types[node] is value and trim_graph.node[node][criteria] < limit:
				trim_graph.remove_node(node)
				#print "removed: ", str(node)
		else:
			if trim_graph.node[node][criteria] < limit:
				trim_graph.remove_node(node)
	return trim_graph

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

def print_top_reciprocated_nodes(graph, count=10, reverse=True, return_graph=False):
	recips = {}
	recip_return = {}
	recip_to_graph=[]
	out_degrees=graph.out_degree() #Not counting the weight of the edges.
	out_degree_to_graph=[] 
	labels = []
	for node in graph.nodes():
		recips[node] = get_reciprocity_of_node(graph, node)
	for w in sorted(recips, key=recips.get, reverse=reverse)[0:count]:
		if not return_graph:
			print graph.node[w]['label'], "&","{0:4f}".format(recips[w]), "\\\\"
		else:
			recip_to_graph.append(recips[w])
			out_degree_to_graph.append(out_degrees[w])
			labels.append(graph.node[w]['label'])
	if return_graph:
		return [out_degree_to_graph, recip_to_graph, labels]

def print_top_self_loops(graph, size=10):
	self_loop_weights = {}
	for self_loop in graph.selfloop_edges():
		weight = graph[self_loop[0]][self_loop[1]]['weight'] # Weight of the self loop
		if not self_loop_weights.has_key(weight):
			self_loop_weights[weight] = [self_loop[0]]
		else:
			self_loop_weights[weight].append(self_loop[0])

	weights_array = self_loop_weights.keys()
	weights_array.sort()
	weights_array.reverse()
	for weight in weights_array[0:size]:     # Returns top self-looping edges for mentions
		print weight,"&",
		if len(self_loop_weights[weight])>1:
			comma=","
		else:
			comma=""
		for j in self_loop_weights[weight]:
			print graph.node[j]['label'], comma,
		print "\\\\"

def show_component_histogram(graph, bins=None, debug=False):
	components = nx.connected_components(graph)
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

if __name__ == '__main__':
	print "Called Proj_Funcs Directly, Nothing to run.  Call from specific module"
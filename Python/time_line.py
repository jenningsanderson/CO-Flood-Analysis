"""Jennings Anderson 2013
CSCI 5352: Final Project: Boulder Flooding

This module is for visualizing the timeline of the flooding for temporal analysis."""

import bf_load as bf
import proj_funcs as f
import networkx as nx
import matplotlib.pyplot as plt
import datetime 
import copy
												# Syntax for what is returned, true/false
query = {	'spec':	 { },						# We want all tweets
			'fields':{	'_id'                   : 0,		# This is the Mongo ID 
						'id'                    : 1,		# This is a number
						'user.screen_name'      : 1, 		# For kicks
						'user.id'               : 1, 		# User ID
						'created_at'			: 1} }		# This is a date, may have to adjust zone.

def get_data_list():
	tweets = bf.query_mongo_get_list(query)

	flood_days = {}
	
	for tweet in tweets:
		tweet['created_at'] -= datetime.timedelta(hours=6) #Adjusting for TimeZone
		this_hour = f.roundTime(tweet['created_at'],roundTo=60*60)
		if flood_days.has_key(this_hour):
			flood_days[this_hour].append(tweet)
		else:
			flood_days[this_hour] = [tweet]
	return flood_days

days = get_data_list()

def make_plot(days):
	to_graph = []
	sorted_keys = days.keys()
	sorted_keys.sort()

	#print sorted_keys
	
	for key in sorted_keys:
		to_graph.append(len(days[key]))

	#max_index = to_graph.index(max(to_graph))
	#print sorted_keys[max_index], to_graph[max_index]

	plt.plot(sorted_keys, to_graph)
	locs, labels = plt.xticks()
	plt.title('Twitter Activity by Day')
	plt.ylabel('Tweets per Day')
	plt.xlabel('Days')
	plt.setp(labels, rotation=90)
	plt.show()

	to_graph_original = copy.deepcopy(to_graph)

	to_graph.sort()
	to_graph.reverse()

	top_ten_hours = []
	for i in to_graph[0:100]:
		top_ten_hours.append(sorted_keys[to_graph_original.index(i)])
		print top_ten_hours[len(top_ten_hours)-1], i


	return top_ten_hours

top_ten_hours = make_plot(days)

print top_ten_hours



# Leads from this Graph: Look at the Twitter activity that happened in the hour with the highest
# activity

# The hours with the most activity:







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

def get_data_list(time_step=60, just_count=True, limit=False):
	'''Returns dictionary:
		Keys: Time Steps
		Values: #Tweets in TimeStep'''
	tweets = bf.query_mongo_get_list(query)

	flood_days = {}
	
	for tweet in tweets:
		tweet['created_at'] -= datetime.timedelta(hours=6) #Adjusting for TimeZone
		this_hour = f.roundTime(tweet['created_at'],roundTo=time_step)
		if flood_days.has_key(this_hour):
			flood_days[this_hour].append(tweet)
		else:
			flood_days[this_hour] = [tweet]
	if just_count:
		for i in flood_days.keys():
			flood_days[i] = len(flood_days[i])
		return flood_days
	else:
		return flood_days

def make_plot_return_top(time_steps, time_step='Day', make_plot=True, limit=100, reverse=True):
	'''Create plot from time_steps dictionary'''
	to_graph = []
	sorted_keys = time_steps.keys()
	sorted_keys.sort()
	
	for key in sorted_keys:
		to_graph.append(len(time_steps[key]))

	if make_plot:
		plt.plot(sorted_keys, to_graph)
		locs, labels = plt.xticks()
		plt.title('Twitter Activity by '+str(time_step)) #Modify this to apply
		plt.ylabel('Tweets per '+str(time_step))		 #Modify this to apply
		plt.xlabel(str(time_step))
		plt.setp(labels, rotation=90)
		plt.show()

	to_graph_original = copy.deepcopy(to_graph)
	to_graph.sort()
	if reverse:
		to_graph.reverse()

	top_times = []
	top_dict = {}
	for i in to_graph[0:limit]:
		top_times.append(sorted_keys[to_graph_original.index(i)])
		top_dict[top_times[len(top_times)-1]] = i
		#print top_times[len(top_times)-1], i

	return top_dict


if __name__ == '__main__':

	minutes = get_data_list(time_step=60, just_count=False)

	#for i in minutes.keys()[0:10]:
	#	print i, len(minutes[i])

	dict = make_plot_return_top(minutes, make_plot=False, limit=15)

	for i in dict.keys()[0:10]:
		print i, dict[i]
	vals = dict.values()
	vals.sort()
	vals.reverse()
	print vals 			#Top minutes with these tweets.

	#test_hours = get_data_list(time_step=60*60)
	#vals = test_hours.values()
	#vals.sort()
	#vals.reverse()
	#print vals
	
	#top_ten = make_plot(hours, 'Hour')

	#for i in top_ten:
	#	print type(i), i
	#print len(top_ten)



# Leads from this Graph: Look at the Twitter activity that happened in the hour with the highest
# activity

# The hours with the most activity:







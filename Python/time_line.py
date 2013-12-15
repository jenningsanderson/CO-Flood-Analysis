"""This module is for visualizing the timeline of the flooding for temporal analysis.
"""

import bf_load as bf
import proj_funcs as f
import networkx as nx
import matplotlib.pyplot as plt
import datetime 
import copy

def get_range(query = bf.all_tweets):
	tweets = bf.query_mongo_get_list(query)
	times = []
	for tweet in tweets:
		tweet['created_at'] -= datetime.timedelta(hours=6) #Adjusting for TimeZone
		times.append(tweet['created_at'])
	times.sort()
	return times

def get_data_list(time_step=60, just_count=True, limit=False):
	'''Returns dictionary:
		Keys: Time Steps
		Values: #Tweets in TimeStep'''
	tweets = bf.query_mongo_get_list(bf.all_tweets)
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
	"""Create plot from time_steps dictionary

	"""
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

	return top_dict


if __name__ == '__main__':

	hours = get_data_list(time_step=60*60, just_count=False)

	dict = make_plot_return_top(hours, make_plot=True, limit=15)

	for i in dict.keys()[0:10]:
		print i, dict[i]
	
	hours = dict.keys()
	hours.sort()


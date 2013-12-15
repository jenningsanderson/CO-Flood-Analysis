"""Jennings Anderson 2013
CSCI 5352: Final Project: Boulder Flooding

This module holds functions used in multiple parts of the analysis project."""

import bf_load as bf
import proj_funcs as f
import networkx as nx
import matplotlib.pyplot as plt
import datetime
import time_line as t
import user_mentions as um
import users_tweets as ut

def hashtag_changes(time_step = 60*60):
	"""Attempting to identify changes in the hashtag structure overtime"""
	ranges = t.get_range()
	first_tweet = ranges[0]
	last_tweet = ranges[len(ranges)-1]
	index = first_tweet

	print first_tweet, last_tweet

	to_graph = []

	while index < last_tweet:
		index += datetime.timedelta(seconds=time_step)
		tweets = bf.get_tweets_between(first_tweet, index)

		graph = ut.create_tweets_graph(tweets)
		print "Tweets before", index, ":", len(tweets)

if __name__ == '__main__':
	hashtag_changes()

	# time_delta = 60*60	#Plotting Hours
	
	# data = t.get_data_list(time_step=time_delta, just_count=False)
	# top_data = t.make_plot_return_top(data, make_plot=False, limit=150, reverse=True)
	# sorted_keys = top_data.keys()
	# sorted_keys.sort()

	# #for i in top_minutes.keys()[0:10]:
	# #	print i, top_minutes[i]			#This is correct, it's just not sorted.
	
	# to_visualize=[]
	# for i in sorted_keys:
	# 	mongo_time = i + datetime.timedelta(hours=6) #Adjusting for timezone
	# 	start = mongo_time - datetime.timedelta(seconds=time_delta)
	# 	end = mongo_time

	# 	print len(data)
		
	# 	umg = um.user_mentions_graph(data)
	# 	to_visualize.append(f.get_graph_reciprocity(umg, weighted=True))


	# plt.plot(sorted_keys, to_visualize, 'r-')
	# locs, labels = plt.xticks()
	# plt.title('Reciprocity by Hour for Non-Geo-Enabled Users') #Modify this to apply
	# plt.ylabel('Reciprocity')		 #Modify this to apply
	# plt.xlabel('Day')
	# plt.setp(labels, rotation=90)
	# plt.show()

"""Jennings Anderson 2013
CSCI 5352: Final Project: Boulder Flooding

This module holds functions used in multiple parts of the analysis project."""

import bf_load as bf
import proj_funcs as f
import networkx as nx
import matplotlib.pyplot as plt
import datetime 
import copy
import time_line as t
import user_mentions as um

if __name__ == '__main__':

	time_delta = 60*60	#Plotting Hours
	
	data = t.get_data_list(time_step=time_delta, just_count=False)
	top_data = t.make_plot_return_top(data, make_plot=False, limit=150, reverse=True)
	sorted_keys = top_data.keys()
	sorted_keys.sort()

	#for i in top_minutes.keys()[0:10]:
	#	print i, top_minutes[i]			#This is correct, it's just not sorted.
	
	to_visualize=[]
	for i in sorted_keys:
		mongo_time = i + datetime.timedelta(hours=6) #Adjusting for timezone
		start = mongo_time - datetime.timedelta(seconds=time_delta)
		end = mongo_time
		query = {	'spec':	{'created_at': {'$gt': start, '$lt': end }, 'geo':{ '$ne' : None } },
			'fields':{	'_id'		:0, 
						'id'		:1, 
						'user.id'	:1, 
						'user.screen_name': 1,
						'entities.user_mentions':1 }	}
		data = bf.query_mongo_get_list(query)
		print len(data)
		
		umg = um.user_mentions_graph(data)
		to_visualize.append(f.get_graph_reciprocity(umg, weighted=True))


	plt.plot(sorted_keys, to_visualize, 'r-')
	locs, labels = plt.xticks()
	plt.title('Reciprocity by Hour for Non-Geo-Enabled Users') #Modify this to apply
	plt.ylabel('Reciprocity')		 #Modify this to apply
	plt.xlabel('Day')
	plt.setp(labels, rotation=90)
	plt.show()

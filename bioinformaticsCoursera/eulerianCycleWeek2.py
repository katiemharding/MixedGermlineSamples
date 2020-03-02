#!/usr/bin/env python3

import random
import sys

# I want to work with the nodes as a tuple (immutable index)
def generate_edges(graph):
	# We need to work with a list of each node and it's following node
	edges=[]
	for node in graph:
		for neighbour in graph[node]:
			edges.append((node,neighbour)) # append node and the following node
			# note this is a tuple, an ordered indexed data type.  Can't change a tuple.
	return(edges)

# I created a function to find the next value from the input list
def NextValue(current_node, nodes_tuple):
	possible_nexts = []
	for node in nodes_tuple: # for each of the nodes provided
		if int(node[0]) == current_node: # find the current node
			possible_nexts.append(node[1]) # note, this will return two values
	next_value = random.choice(possible_nexts) # I return one at random
	return(next_value)

def eulerianCycle(graph):
	n = random.choice(list(graph.keys()))
	nodes_tuple = generate_edges(node_dict)
	current_node = n
	circuit_list = [] # answer 
	stack = [] # collection of the list

	while True:
		if any(current_node == x[0] for x in nodes_tuple) == False:
			# False only happens when nodes_tuple is empty (no where to go)
			# if the nodes tuple is broken, it will go here with remaining nodes
			# this appends stack to circuit until stack is empty
			circuit_list.append(current_node) # add the last position to the list
			# note this will be backwards
			if stack==[]:
				break # stop if stack is empty and there are no new positions after all have been used
			current_node = stack[-1] # go back one item
			#print(current_node, "current node fase")
			stack.pop() # remove the last item from the list
            
		else:
			stack.append(current_node) # add this random value to the stack
			nextV=NextValue(int(current_node),nodes_tuple)  # find the next node
			nodes_tuple.remove((current_node,nextV)) # remove the "used" value from the list
			current_node = nextV # start over with next value
			# this secton runs until nodes_tuple is empty
	return(circuit_list[::-1])

if __name__ == '__main__':
	## first get the data, and create a dictionary (multiple paths from node seperated by commas)
	# input_list = [line.rstrip() for line in sys.stdin]
	new_file = open(sys.argv[1])
	# creates a dictionary from each line in the file
	node_dict = dict((line.strip().split(' -> ') for line in new_file)) 
	print(node_dict, "node dict")
	for node in node_dict: 
		# splits the nodes so that if there are two paths from a node, they appear as a list seperated by a omma
		node_dict[node] = node_dict[node].split (',') 
	
	answer =eulerianCycle(node_dict)
	print("->".join(answer))


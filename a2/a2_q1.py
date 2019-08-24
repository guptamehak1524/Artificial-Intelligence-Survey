import random


def addKey(dict,key):
	dict[key] = list()

def addValue(dict,key,value):
	dict[key].append(value)

def rand_graph(n,p):
	rand_graph = {}
	for i in range(n):
		addKey(rand_graph, i)
	for i in range(n):
		for j in range(n):
			if i != j:
				if j in rand_graph[i]:
					continue
				r = random.random()
				if r<= p:
					addValue(rand_graph,i,j)
					addValue(rand_graph,j,i)
				else: 
					continue
	return rand_graph
 



def check_teams(graph, csp_sol):
	for key in graph:
		for value in graph[key]:
			if csp_sol[key] == csp_sol[value]:
 				return False 
	return True


graph1 = {0: [3, 1], 1: [0, 4, 2], 2: [1], 3: [0, 4], 4: [1, 3]}
csp_sol1 = {0: 0, 1: 1, 2: 0, 3: 1, 4: 0}

print(check_teams(graph2, csp_sol2))


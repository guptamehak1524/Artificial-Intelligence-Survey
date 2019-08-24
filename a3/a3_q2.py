import os
import copy
import time
from a2_q1 import *

sentence = ""
count = 0

# LOGIC APPLIED
# make_ice_breaker_sat takes a graph and k teams as input and produces results as follows : 
#  1. Every variable has equal possibility of being in any of the k teams so 
#  every unique variable combined with the team is assigned a unique variable
#  For example
#  ({0: [1,2], 1:[0], 2:[0],3[]}, 3)
#  Person 0 - Team 1 = 1
#  Person 0 - Team 2 = 2
#  Person 0 - Team 3 = 3
#  Person 1 - Team 1 = 4
#  Person 1 - Team 2 = 5
#  Person 1 - Team 3 = 6
#  and so on and after that the problem is divided into 3 sub functions to get all the constraints

def make_ice_breaker_sat(graph, k):
	global sentence
	global count
	
	input = 1
	for key in graph:
		variables = []
		for i in range(k):
			variables.append(str(input))
			input += 1
		at_least_one_team(variables)
		at_most_one_team(variables)
	different_team_for_friends(graph,k)
	sentence = 'c Ice Breaker Problem  \np cnf ' + str(len(graph)*k) + ' '+ str(count) + '\n' + sentence
	return sentence


#  Every Person is assigned a team
def at_least_one_team(k):
	global sentence
	global count
	for i in k:
		sentence += i + ' '
	sentence += '0\n'
	count += 1

# Every person is assigned exactly one team
def at_most_one_team(k):
	global sentence
	global count
	l = 1
	for i in k:
		for j in k[l:]:
		 	sentence = sentence + '-' + i + ' ' + '-' + j + ' '+ '0\n'
		 	count += 1
		l = l + 1

# This function keeps track of all the friends and makes sure no 2 friends are in the same team
def different_team_for_friends(graph,k):
	global sentence
	global count
	for key in graph:
		for val in graph[key]:
			graph[val].remove(key)
			for i in range(k):
				sentence += '-' + str(key*k+i+1) + ' ' + '-' + str(val*k+i+1) + ' ' + '0\n'
				count += 1


#  Find_min_teams uses the  make_ice_breaker_sat to get the minimum number of teams
#  required to put all the people in
#  Time frames are added for getting data for excel sheets
def find_min_teams(graph):
    global sentence
    global count
    start_time = time.time()
    for i in range(len(graph)):
    	print("----")
    	print(i)
    	print("----")
    	sentence = " "
    	count = 0
    	result = make_ice_breaker_sat(copy.deepcopy(graph), i)
    	text_file = open("Output.txt", "w")
    	text_file.write(result)
    	text_file.close()
    	os.system('minisat Output.txt out')
    	read_file = open("out","r")
    	output = read_file.read(3)
    	read_file.close()
    	if output == "SAT":
    		print("-----------------------------------------")
    		print(i)
    		print("-----------------------------------------")
    		elapsed_time = time.time()
    		print(elapsed_time - start_time)
    		print("-----------------------------------------")
    		return i


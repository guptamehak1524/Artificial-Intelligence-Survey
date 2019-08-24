# ASSIGNMENT 3
# DATE - JUNE 26, 2019
# MEHAK GUPTA
# 301311972

import numpy as np
import math  
import time
import os

sentence = ''
count =0

# make_queen_sat takes N and created a matrix of N*N Variables
# All the rows, columns and diagonals are solved under separate functions
def make_queen_sat(N):
	global sentence
	global count
	w, h = N, N;
	Matrix = [[0 for x in range(w)] for y in range(h)] 
	input = 0 
	for i in range(N):
		for j in range(N):
			Matrix[i][j] = input + 1
			input += 1
	solve_rows(Matrix)
	solve_columns(Matrix)
	solve_diagonals(Matrix)
	sentence = 'c '+ str(N) +'-queens problem \np cnf ' + str(N*N) + ' '+ str(count) + '\n' + sentence
	return sentence


# for each row of the matrix exactly one variable is chosen
def solve_rows(Matrix):
	for i in Matrix:
		exactly_one(i)


# for each column of the matrix exactly one variable is chosen
def solve_columns(Matrix):
	column_Matrix = [[Matrix[j][i] for j in range(len(Matrix))] for i in range(len(Matrix[0]))] 
	for i in column_Matrix:
		exactly_one(i)


# for each diagonal of the matrix one or no variable is chosen
def solve_diagonals(Matrix):
	new = np.array(Matrix)
	diags = [new[::-1,:].diagonal(i) for i in range(-new.shape[0]+2,new.shape[1]-1)]
	diags.extend(new.diagonal(i) for i in range(new.shape[1]-2,-new.shape[0]+1,-1))
	diagonal_Matrix  = [n.tolist() for n in diags]
	for i in diagonal_Matrix:
		at_most_one(i)


# supporting function for rows and columns that helps to chose exactly one variable
def exactly_one(contraints):
	global sentence
	global count
	k = 1
	for i in contraints:
		for j in contraints[k:]:
		 	sentence = sentence + "-" + str(i) + ' '+ "-" + str(j) + ' '+ '0\n'
		 	count += 1
		k = k + 1
	for i in contraints:
		sentence += str(i) + ' '
	sentence += '0' + '\n'
	count += 1	 	

# supporting function that helps to chose one or no variable
def at_most_one(contraints):
	global sentence
	global count
	k = 1
	for i in contraints:
		for j in contraints[k:]:
		 	sentence = sentence + "-" + str(i) + ' '+ "-" + str(j) + ' '+ '0\n'
		 	count += 1
		k = k + 1


# Part 2 of Question 1 of the Assignment where function take a string which is solution 
# to the minisat and returns a visual representation of the same
def draw_queen_sat_sol(sol):
	if(sol == "UNSAT"):
		print("no solution")
	sol = sol.split(' ')
	N = int(math.sqrt(len(sol)))
	if N > 40:
		print("Too big: N must be less than 40")
	else:
		count = 1
		for i in sol:
			if int(i) < 0:
				print('.', end =" ")
			if int(i) > 0:
				print('Q', end =" ")
			if count % N == 0:
				print('\n')
			count += 1


# extra function to run the 10 sec experiment 
def ten_second_experiment():
	global sentence 
	global count
	for i in range(2,50):
		start_time =  time.time()
		sentence = " "
		count  = 0
		result = make_queen_sat(i)
		text_file = open("Output.txt", "w")
		text_file.write(result)
		text_file.close()
		os.system('minisat Output.txt out')
		read_file = open("out","r")
		output = read_file.read(3)
		if output == "SAT":
			for line in read_file:
				sol = line.strip()
			read_file.close()
			draw_queen_sat_sol(sol)
			elapsed_time = time.time()
			print("______________________________________")
			print(i)
			print( elapsed_time - start_time)
			print("______________________________________")
		else:
			read_file.close()
			elapsed_time = time.time()
			print(i)
			print("______________________________________")
			print( elapsed_time - start_time)
			print("______________________________________")



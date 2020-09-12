import os
import math
import numpy as np


lkh_dir = '/LKH/LKH-2.0.9/'
tsplib_dir = '/TSPLIB/'
lkh_cmd = 'LKH'
pwd= os.path.dirname(os.path.abspath(__file__))


def writeTSPLIBfile(tsp_fname,CostMatrix,test_comment):

	tsp_dim = len(CostMatrix)
	display_data_type_line ='DISPLAY_DATA_TYPE: ' + 'NO_DISPLAY' + '\n' # 'NO_DISPLAY'
	Cost_Matrix_STRline = []
	for i in range(0,tsp_dim):
		cost_matrix_strline = ''
		for j in range(0,tsp_dim-1):
			cost_matrix_strline = cost_matrix_strline + str(int(CostMatrix[i][j])) + ' '

		j = tsp_dim-1
		cost_matrix_strline = cost_matrix_strline + str(int(CostMatrix[i][j]))
		cost_matrix_strline = cost_matrix_strline + '\n'
		Cost_Matrix_STRline.append(cost_matrix_strline)
	
	problem_file = open((pwd + tsplib_dir + tsp_fname + '.tsp'), "w")
	print('Test: ' + tsp_fname)
	problem_file.write('NAME: ' + tsp_fname + '\n')
	problem_file.write('COMMENT : ' + test_comment + '\n')
	problem_file.write('TYPE : TSP' + '\n')
	problem_file.write('DIMENSION : ' + str(tsp_dim) + '\n')
	problem_file.write('EDGE_WEIGHT_TYPE : ' + 'EXPLICIT' + '\n')
	problem_file.write('EDGE_WEIGHT_FORMAT: ' + 'FULL_MATRIX' + '\n')
	problem_file.write('EDGE_WEIGHT_SECTION' + '\n')
	for i in range(0,len(Cost_Matrix_STRline)):
		problem_file.write(Cost_Matrix_STRline[i])

	problem_file.write('EOF\n')
	problem_file.close()

	parameter_file = open((pwd + tsplib_dir + tsp_fname + '.par'), "w")

	problem_file_line = 'PROBLEM_FILE = ' + pwd + tsplib_dir + tsp_fname + '.tsp' + '\n' # remove pwd + tsplib_dir
	optimum_line = 'OPTIMUM 378032' + '\n'
	move_type_line = 'MOVE_TYPE = 5' + '\n'
	patching_c_line = 'PATCHING_C = 3' + '\n'
	patching_a_line = 'PATCHING_A = 2' + '\n'
	runs_line = 'RUNS = 10' + '\n'
	tour_file_line = 'TOUR_FILE = ' + tsp_fname + '.txt' + '\n'

	parameter_file.write(problem_file_line)
	parameter_file.write(optimum_line)
	parameter_file.write(move_type_line)
	parameter_file.write(patching_c_line)
	parameter_file.write(patching_a_line)
	parameter_file.write(runs_line)
	parameter_file.write(tour_file_line)
	parameter_file.close()
	return problem_file, parameter_file

def copy_to_TSPLIBdir(file_name):
	copy_toTSPLIBdir_cmd = 'cp' + ' ' + pwd + '/' + file_name + '.txt' + ' ' +  pwd + tsplib_dir
	os.system(copy_toTSPLIBdir_cmd)

def run_LKH(file_name):
	run_lkh_cmd =  pwd + lkh_dir + lkh_cmd + ' ' + pwd + tsplib_dir + file_name + '.par'
	os.system(run_lkh_cmd)

def rm_solution_file_cmd(file_name):
	rm_sol_cmd = 'rm' + ' ' + pwd + '/' + file_name + '.txt'
	os.system(rm_sol_cmd) 


if __name__ == "__main__":
	cost_matrix = np.array([[ 0, 32, 53, 51, 84, 72, 76, 33, 33, 64],
                            [32,  0, 21, 29, 76, 40, 43, 41, 36, 37],
                            [53, 21,  0, 23, 72, 19, 23, 52, 46, 22],
                            [51, 29, 23,  0, 50, 35, 39, 36, 30, 14],
                            [84, 76, 72, 50,  0, 79, 83, 51, 51, 53],
                            [72, 40, 19, 35, 79,  0,  4, 69, 63, 26],
                            [76, 43, 23, 39, 83,  4,  0, 74, 67, 30],
                            [33, 41, 52, 36, 51, 69, 74,  0,  6, 50],
                            [33, 36, 46, 30, 51, 63, 67,  6,  0, 44],
                            [64, 37, 22, 14, 53, 26, 30, 50, 44, 0]])

	tsp_fname = "test"
	test_comment = "test run"

	[problem_file, parameter_file] = writeTSPLIBfile(tsp_fname,cost_matrix,test_comment)
	copy_to_TSPLIBdir(tsp_fname)
	run_LKH(tsp_fname)
	rm_solution_file_cmd(tsp_fname)
import time
from tsp_algorithms import solve_tsp
from utils import generate_matrix, print_matrix, print_solution
import cProfile



if __name__ == '__main__':
    matrix = generate_matrix(22)
    # print_matrix(matrix)
    
    # cProfile.run('solve_tsp(matrix, \'little\')', sort='time')

    for method in ['little', 'nearest']:
        start_time = time.time()
        best_solution = solve_tsp(matrix, method)
        end_time = time.time()
        print_solution(method, best_solution, end_time - start_time)
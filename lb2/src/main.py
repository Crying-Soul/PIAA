import time
from tsp_algorithms import solve_tsp
from utils import generate_matrix, print_matrix, print_solution, export_matrix, load_matrix


if __name__ == '__main__':
    matrix = generate_matrix(size=5, seed=52, symmetric=False)
    print_matrix(matrix)
    # export_matrix(matrix, 'matrix', file_type='csv')
    # matrix = load_matrix('matrix', 'csv')

    verbose = True  

    for method in ['little', 'nearest']:
        start_time = time.time()
        best_solution = solve_tsp(matrix, method, verbose=verbose)
        end_time = time.time()
        print_solution(method, best_solution, end_time - start_time)
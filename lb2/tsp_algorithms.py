import heapq
import numpy as np
from math import inf



def reduce_cost_matrix(matrix, verbose=False):
    reduced_matrix = matrix.copy()
    row_min = np.min(reduced_matrix, axis=1)
    row_min[np.isinf(row_min)] = 0
    reduced_matrix -= row_min[:, None]
    
    col_min = np.min(reduced_matrix, axis=0)
    col_min[np.isinf(col_min)] = 0
    reduced_matrix -= col_min
    
    if verbose:
        print("=== Редукция матрицы ===")
        print(f"Минимумы строк: {row_min}")
        print(f"Минимумы столбцов: {col_min}")
        print(f"Редуцированная матрица:\n{reduced_matrix}")
    
    return reduced_matrix, np.sum(row_min) + np.sum(col_min)

def minimum_spanning_tree(matrix, vertices, verbose=False):
    if len(vertices) <= 1:
        return 0.0
    total_cost = 0.0
    visited = set()
    start = next(iter(vertices))
    priority_queue = [(0.0, start)]
    
    if verbose:
        print(f"=== Вычисление MST для вершин {vertices} ===")
    
    while priority_queue:
        weight, u = heapq.heappop(priority_queue)
        if u in visited:
            continue
        total_cost += weight
        visited.add(u)
        for v in vertices - visited:
            edge_weight = matrix[u][v]
            if edge_weight != inf:
                heapq.heappush(priority_queue, (edge_weight, v))
                if verbose:
                    print(f"Добавлено ребро {u} -> {v} с весом {edge_weight}")
    
    if verbose:
        print(f"MST оценка оставшихся вершин: {total_cost}")
    
    return total_cost if len(visited) == len(vertices) else inf

def tsp_branch_and_bound(matrix, current, visited, current_cost, path, best, selected_edges, verbose=False):
    num_cities = len(matrix)
    
    if len(visited) == num_cities:
        if matrix[current][0] == inf:
            return
        total_cost = current_cost + matrix[current][0]
        if total_cost < best['cost']:
            best['cost'] = total_cost
            best['path'] = path + [0]
        if verbose:
            print(f"✅ Найден полный путь {path + [0]} с общей стоимостью {total_cost}")
        return

    candidates = [(city, matrix[current][city]) for city in range(num_cities) 
                  if city not in visited and matrix[current][city] != inf]
    candidates.sort(key=lambda x: x[1])

    for next_city, cost_to_next in candidates:
        new_matrix = matrix.copy()
        new_matrix[current, :] = inf  
        new_matrix[:, next_city] = inf  
        
        if len(visited) + 1 < num_cities:
            new_matrix[next_city][0] = inf  

        if current in selected_edges:
            prev_city = selected_edges[current]
            new_matrix[next_city][prev_city] = inf  

        selected_edges[current] = next_city

        reduced_matrix, reduced_cost = reduce_cost_matrix(new_matrix, verbose)
        new_cost = current_cost + cost_to_next + reduced_cost

        remaining_cities = set(range(num_cities)) - visited - {next_city}
        mst_estimate = minimum_spanning_tree(reduced_matrix, remaining_cities, verbose) if remaining_cities else 0

        min_edges_sum = sum(sorted([min(row[row != inf]) for i, row in enumerate(reduced_matrix) if i in remaining_cities])[:2])

        lower_bound = new_cost + min(mst_estimate, min_edges_sum)
        
        if verbose:
            print(f"🔍 Рассматриваем путь {path + [next_city]} (стоимость: {new_cost}, нижняя граница: {lower_bound})")
        
        if lower_bound < best['cost']:
            tsp_branch_and_bound(reduced_matrix, next_city, visited | {next_city}, new_cost, path + [next_city], best, selected_edges.copy(), verbose)

def tsp_little_algorithm(matrix, verbose=False):
    if verbose:
        print("🚀 Запуск алгоритма Литтла...")
    best_solution = {'cost': inf, 'path': []}
    reduced_matrix, initial_cost = reduce_cost_matrix(matrix, verbose)
    tsp_branch_and_bound(reduced_matrix, 0, {0}, initial_cost, [0], best_solution, {}, verbose)
    return best_solution

def tsp_nearest_neighbor(matrix, verbose=False):
    num_cities = len(matrix)
    visited = {0}
    path = [0]
    total_cost = 0
    current_city = 0
    while len(visited) < num_cities:
        next_city = min((i for i in range(num_cities) if i not in visited), key=lambda i: matrix[current_city][i], default=None)
        if next_city is None or matrix[current_city][next_city] == inf:
            return {'cost': inf, 'path': []}
        visited.add(next_city)
        path.append(next_city)
        total_cost += matrix[current_city][next_city]
        current_city = next_city
    if matrix[current_city][0] == inf:
        return {'cost': inf, 'path': []}
    path.append(0)
    total_cost += matrix[current_city][0]
    if verbose:
        print(f"🏁 Оптимальный путь найден: {path}, стоимость: {total_cost}")
    return {'cost': total_cost, 'path': path}

def solve_tsp(matrix, method='little', verbose=False):
    return tsp_little_algorithm(matrix, verbose) if method == 'little' else tsp_nearest_neighbor(matrix, verbose)

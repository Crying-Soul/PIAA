import numpy as np
from tabulate import tabulate
from colorama import Fore, Style

INF = float('inf')

def city_index_to_name(index):
    """Конвертирует индекс города в его буквенное обозначение (A, B, C и т. д.)."""
    return chr(ord('A') + index)

def generate_matrix(size):
    """Генерирует матрицу размера size x size."""
    np.random.seed(99)  
    matrix = np.random.randint(1, 100, size=(size, size)).astype(float)
    np.fill_diagonal(matrix, INF)
    return matrix


def print_matrix(matrix):
    """Выводит матрицу расстояний в удобочитаемом виде."""
    headers = [city_index_to_name(i) for i in range(len(matrix))]
    table = tabulate(matrix, headers=headers, showindex=headers, tablefmt="grid", numalign="right")
    print(f"{Fore.CYAN}Матрица расстояний:{Style.RESET_ALL}\n{table}\n")

def print_solution(method, best_solution, elapsed_time):
    """Выводит решение в красивом формате."""
    path_str = f"{Fore.GREEN} → {Style.RESET_ALL}".join(city_index_to_name(i) for i in best_solution['path'])
    print(f"{Fore.YELLOW}Метод:{Style.RESET_ALL} {method.capitalize()}")
    print(f"{Fore.MAGENTA}Лучшая стоимость пути:{Style.RESET_ALL} {best_solution['cost']}")
    print(f"{Fore.BLUE}Оптимальный маршрут:{Style.RESET_ALL} {path_str}")
    print(f"{Fore.RED}Время выполнения:{Style.RESET_ALL} {elapsed_time:.4f} секунд\n")
    print("=" * 50)
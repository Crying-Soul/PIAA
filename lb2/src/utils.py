import numpy as np
from tabulate import tabulate
from colorama import Fore, Style

INF = float('inf')

def city_index_to_name(index):
    """Конвертирует индекс города в его буквенное обозначение (A, B, C и т. д.).
    
    Аргументы:
    index -- индекс города (int)
    
    Возвращает:
    Буквенное обозначение города (str)
    """
    return chr(ord('A') + index)

def generate_matrix(size, seed=None, symmetric=False):
    """
    Генерирует квадратную матрицу размера size x size со случайными значениями.
    
    Аргументы:
      size -- размер матрицы (int)
      seed -- начальное значение для генератора случайных чисел (int, по умолчанию None)
      symmetric -- если True, генерируется симметричная матрица (bool, по умолчанию False)
    
    Возвращает:
      matrix -- сгенерированная матрица (numpy.ndarray), где диагональные элементы равны INF
    """
    if seed is not None:
        np.random.seed(seed)
    matrix = np.random.randint(1, 100, size=(size, size)).astype(float)
    
    if symmetric:
        i_lower = np.tril_indices(size, -1)
        matrix[i_lower] = matrix.T[i_lower]
    
    np.fill_diagonal(matrix, INF)
    return matrix

def export_matrix(matrix, filename='export_matrix', file_type="txt"):
    """
    Экспортирует матрицу в заданный файл в зависимости от формата.
    
    Аргументы:
      matrix -- матрица (numpy.ndarray)
      filename -- имя файла (str), без расширения
      file_type -- тип файла для экспорта ("txt", "csv", "npy")
    
    Исключения:
      ValueError -- если передан неподдерживаемый тип файла или matrix не является numpy.ndarray
    """
    if not isinstance(matrix, np.ndarray):
        raise ValueError("Input matrix must be a numpy.ndarray")
    
    filename_with_extension = f"{filename}.{file_type}"
    
    if file_type == "txt":
        np.savetxt(filename_with_extension, matrix, fmt='%g')
    elif file_type == "csv":
        np.savetxt(filename_with_extension, matrix, delimiter=",", fmt='%g')
    elif file_type == "npy":
        np.save(filename_with_extension, matrix)
    else:
        raise ValueError(f"Unsupported file type: {file_type}. Supported types are 'txt', 'csv', 'json', 'npy'.")
    
    print(f"Matrix successfully exported to {filename_with_extension}")

def load_matrix(filename, file_type="txt"):
    """
    Загружает матрицу из файла в зависимости от формата.
    
    Аргументы:
      filename -- имя файла (str), без расширения
      file_type -- тип файла для импорта ("txt", "csv", "json", "npy")
    
    Возвращает:
      matrix -- загруженная матрица (numpy.ndarray)
    
    Исключения:
      ValueError -- если передан неподдерживаемый тип файла
    """
    filename_with_extension = f"{filename}.{file_type}"
    
    if file_type == "txt":
        matrix = np.loadtxt(filename_with_extension)
    elif file_type == "csv":
        matrix = np.loadtxt(filename_with_extension, delimiter=",")
    elif file_type == "npy":
        matrix = np.load(filename_with_extension)
    else:
        raise ValueError(f"Unsupported file type: {file_type}. Supported types are 'txt', 'csv', 'npy'.")
    
    return matrix


def print_matrix(matrix):
    """Выводит матрицу расстояний в удобочитаемом виде с использованием цветного форматирования.
    
    Аргументы:
    matrix -- матрица расстояний (numpy.ndarray)
    """
    headers = [city_index_to_name(i) for i in range(len(matrix))]
    table = tabulate(matrix, headers=headers, showindex=headers, tablefmt="grid", numalign="right")
    print(f"{Fore.CYAN}Матрица расстояний:{Style.RESET_ALL}\n{table}\n")

def print_solution(method, best_solution, elapsed_time):
    """Выводит решение задачи коммивояжера в красивом формате с использованием цветного форматирования.
    
    Аргументы:
    method -- метод решения (str)
    best_solution -- лучший найденный путь и его стоимость (dict)
    elapsed_time -- время выполнения алгоритма (float)
    """
    path_str = f"{Fore.GREEN} → {Style.RESET_ALL}".join(city_index_to_name(i) for i in best_solution['path'])
    print(f"{Fore.YELLOW}Метод:{Style.RESET_ALL} {method.capitalize()}")
    print(f"{Fore.MAGENTA}Лучшая стоимость пути:{Style.RESET_ALL} {best_solution['cost']}")
    print(f"{Fore.BLUE}Оптимальный маршрут:{Style.RESET_ALL} {path_str}")
    print(f"{Fore.RED}Время выполнения:{Style.RESET_ALL} {elapsed_time:.4f} секунд\n")
    print("=" * 50)
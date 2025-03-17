from colorama import Fore, Back, Style, init
init(autoreset=True)

def kmp_search(text, pattern, verbose=False):
    """
    Реализует алгоритм КМП для поиска вхождения pattern в text.
    Возвращает индекс первого вхождения или -1, если вхождение не найдено.
    """
    n = len(pattern)
    lps = [0] * n  # lps[i] — длина наибольшего собственного префикса, совпадающего с суффиксом pattern[0:i+1]
    length = 0  # длина предыдущего совпадающего префикса
    i = 1

    # Промежуточный вывод для LPS
    if verbose:
        print(Fore.CYAN + "\n=== Вычисление массива LPS ===")
    
    while i < n:
        if verbose:
            print(Fore.YELLOW + f"Шаг {i}: Сравниваем pattern[{i}] = {pattern[i]} с pattern[{length}] = {pattern[length]}")
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
            if verbose:
                print(Fore.GREEN + f"Совпадение! Устанавливаем lps[{i-1}] = {length}")
        else:
            if length != 0:
                length = lps[length - 1]
                if verbose:
                    print(Fore.RED + f"Несовпадение! Уменьшаем длину префикса до lps[{length}]")
            else:
                lps[i] = 0
                i += 1
                if verbose:
                    print(Fore.RED + f"Несовпадение! Устанавливаем lps[{i-1}] = 0 и увеличиваем i")

    if verbose:
        print(Fore.MAGENTA + f"\nИтоговый массив LPS: {lps}\n")
    
    # Поиск pattern в text
    i = 0  # индекс для text
    j = 0  # индекс для pattern
    m = len(text)

    if verbose:
        print(Fore.CYAN + "\n=== Поиск совпадений в тексте ===")

    while i < m:
        if verbose:
            print(Fore.YELLOW + f"Шаг {i}: Сравниваем text[{i}] = {text[i]} с pattern[{j}] = {pattern[j]}")
        
        if pattern[j] == text[i]:
            i += 1
            j += 1
            if verbose:
                print(Fore.GREEN + f"Совпадение! Переходим к следующему символу: i = {i}, j = {j}")
            if j == n:
                if verbose:
                    print(Fore.GREEN + f"Найдено вхождение! Возвращаем индекс {i - j}")
                return i - j  # найдено вхождение, возвращаем индекс начала
        else:
            if j != 0:
                j = lps[j - 1]
                if verbose:
                    print(Fore.RED + f"Несовпадение! Переходим на j = {j} согласно lps")
            else:
                i += 1
                if verbose:
                    print(Fore.RED + f"Несовпадение! Увеличиваем i: i = {i}")
    
    if verbose:
        print(Fore.MAGENTA + "Вхождение не найдено.")
    return -1

from test_cycle import *
def main():
    # Считываем строки строго в порядке ввода:
    # первая строка - A, вторая строка - B.
    A = A1
    B = B1

    verbose = True  # Установите в True для вывода шагов

    # Проверка длины строк
    if len(A) != len(B):
        print(Fore.RED + -1)
        return

    # Если строки совпадают, циклический сдвиг равен 0.
    if A == B:
        print(Fore.GREEN + 0)
        return

    # Проверяем, является ли A циклическим сдвигом B.
    # Для этого ищем A в строке B+B.
    text = B + B
    pos = kmp_search(text, A, verbose)
    
    # Если найденное вхождение начинается в пределах длины строки B,
    # вычисляем сдвиг.
    if pos != -1 and pos < len(B):
        print(Fore.GREEN + f"Циклический сдвиг: {(len(B) - pos) % len(B)}")
    else:
        print(Fore.RED + -1)

if __name__ == '__main__':
    main()

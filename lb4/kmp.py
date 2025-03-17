from colorama import Fore, Back, Style, init
init(autoreset=True)

def compute_lps(pattern, verbose=False):
    """
    Вычисляет массив LPS (Longest Prefix Suffix).
    LPS[i] хранит длину наибольшего собственного префикса, который является суффиксом строки pattern[:i+1].
    """
    m = len(pattern)
    lps = [0] * m
    length = 0  
    i = 1  

    if verbose:
        print(Fore.CYAN + "\n=== Вычисление LPS ===")
    
    while i < m:
        if verbose:
            print(Fore.YELLOW + f"\nШаг {i}: Текущая длина префикса {length}. Пытаемся сравнить pattern[{i}] = {pattern[i]} с pattern[{length}] = {pattern[length]}")

        if pattern[i] == pattern[length]:  
            length += 1
            lps[i] = length
            i += 1
            if verbose:
                print(Fore.GREEN + f"  Совпадение! Устанавливаем lps[{i-1}] = {length}")
        elif length:  
            length = lps[length - 1]  
            if verbose:
                print(Fore.RED + f"  Несовпадение! Уменьшаем длину префикса до lps[{length}]")
        else:
            lps[i] = 0  
            i += 1
            if verbose:
                print(Fore.RED + f"  Несовпадение! Устанавливаем lps[{i-1}] = 0 и увеличиваем i")

    if verbose:
        print(Fore.MAGENTA + f"\nИтоговый массив LPS: {lps}\n")
    
    return lps

def kmp_search(text, pattern, verbose=False):
    """
    Реализация алгоритма Кнута-Морриса-Пратта для поиска подстроки в строке.
    Возвращает список индексов начала всех вхождений pattern в text.
    """
    n, m = len(text), len(pattern)
    if m == 0:
        return list(range(n + 1))

    lps = compute_lps(pattern, verbose)
    indices = []
    i = j = 0  

    if verbose:
        print(Fore.CYAN + "\n=== Поиск KMP ===")

    while i < n:
        if verbose:
            print(Fore.YELLOW + f"\nШаг {i}: Сравниваем text[{i}] = {text[i]} с pattern[{j}] = {pattern[j]}")
        
        if text[i] == pattern[j]:  
            i += 1
            j += 1
            if verbose:
                print(Fore.GREEN + f"  Совпадение! Переходим к следующему символу: i = {i}, j = {j}")

        if j == m:  
            indices.append(i - j)  
            if verbose:
                print(Fore.GREEN + f"  => Найдено вхождение на индексе {i - j}")
            j = lps[j - 1]  

        elif i < n and text[i] != pattern[j]:  
            if j:
                j = lps[j - 1]  
                if verbose:
                    print(Fore.RED + f"  Несовпадение! Переходим на j = {j} согласно lps")
            else:
                i += 1  
                if verbose:
                    print(Fore.RED + f"  Несовпадение! Увеличиваем i: i = {i}")

    if verbose:
        print(Fore.MAGENTA + f"\nИтоговые индексы вхождений: {indices}")
    
    return indices

from test_kmp import *
if __name__ == "__main__":
    pattern = pattern5
    text = text5
    
    verbose = True

    result = kmp_search(text, pattern, verbose)

    print(",".join(map(str, result)) if result else -1)

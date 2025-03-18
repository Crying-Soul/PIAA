from colorama import Fore, Back, Style, init # type: ignore
init(autoreset=True)

from colorama import Fore

def compute_lps(pattern, verbose=False):
    """
    Вычисляет массив LPS (Longest Prefix Suffix).
    LPS[i] хранит длину наибольшего собственного префикса, который является суффиксом pattern[:i+1].
    """
    m = len(pattern)
    lps = [0] * m
    length = 0  # Длина предыдущего совпадающего префикса
    i = 1  # Начинаем со второго символа

    if verbose:
        print(Fore.CYAN + "\n=== Вычисление LPS ===")
    
    while i < m:
        if verbose:
            print(Fore.YELLOW + f"Шаг {i}: Текущая длина префикса {length}. Сравниваем pattern[{i}] = {pattern[i]} с pattern[{length}] = {pattern[length] if length < i else 'N/A'}")
        
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
            if verbose:
                print(Fore.GREEN + f"  Совпадение! Устанавливаем lps[{i-1}] = {length}")
        else:
            if length != 0:
                length = lps[length - 1]  # Откатываемся назад
                if verbose:
                    print(Fore.RED + f"  Несовпадение! Откатываемся к lps[{length}]")
            else:
                lps[i] = 0
                i += 1
                if verbose:
                    print(Fore.RED + f"  Несовпадение! Устанавливаем lps[{i-1}] = 0")
    
    if verbose:
        print(Fore.MAGENTA + f"\nИтоговый массив LPS: {lps}\n")
    
    return lps

from colorama import Fore

def kmp_search(text, pattern, verbose=False):
    """
    Реализация алгоритма Кнута-Морриса-Пратта для поиска подстроки в строке.
    Возвращает список индексов начала всех вхождений pattern в text.
    """
    n, m = len(text), len(pattern)
    if m == 0:
        return list(range(n + 1))
    
    # Вычисляем массив LPS (без вывода промежуточных сообщений)
    lps = compute_lps(pattern, verbose=False)
    
    indices = []
    i, j = 0, 0  # i - индекс в text, j - индекс в pattern
    
    if verbose:
        print(Fore.CYAN + "\n=== Поиск KMP ===")
    
    while i < n:
        # Если символы совпадают, переходим к следующему символу
        if text[i] == pattern[j]:
            if verbose:
                print(Fore.YELLOW + f"\nШаг {i}: Сравниваем text[{i}] = {text[i]} с pattern[{j}] = {pattern[j]}")
                print(Fore.GREEN + f"  Совпадение! Переходим к следующему символу: i = {i+1}, j = {j+1}")
            i += 1
            j += 1
            
            # Если найдено полное совпадение, сохраняем индекс и продолжаем поиск
            if j == m:
                indices.append(i - j)
                if verbose:
                    print(Fore.GREEN + f"  => Найдено вхождение на индексе {i - j}")
                j = lps[j - 1]
        else:
            # Если происходит несовпадение, выводим информацию и корректируем индекс pattern
            if verbose:
                print(Fore.YELLOW + f"\nШаг {i}: Сравниваем text[{i}] = {text[i]} с pattern[{j}] = {pattern[j]}")
            if j != 0:
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
    pattern = "лилила"
    text = "лилилось лилилась"
    
    verbose = True

    result = kmp_search(text, pattern, verbose)

    # print(",".join(map(str, result)) if result else -1)

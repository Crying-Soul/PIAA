from colorama import init, Fore, Back, Style

# Инициализация colorama (обязательно для корректного отображения в Windows)
init(autoreset=True)

def levenshtein_distance(s, t, special_replacer, special_replace_cost, special_deletion_symbol, special_deletion_cost, verbose=False):
    n, m = len(s), len(t)
    # Создаём матрицу (n+1) x (m+1)
    dp = [[0] * (m + 1) for _ in range(n + 1)]

    # Функция для стоимости удаления символа из s
    def deletion_cost(ch):
        return special_deletion_cost if ch == special_deletion_symbol else 1

    # Функция для стоимости замены
    def substitution_cost(ch_source, ch_target):
        if ch_source == ch_target:
            return 0
        return special_replace_cost if ch_target == special_replacer else 1

    if verbose:
        print(Fore.YELLOW + "\n=== ИНИЦИАЛИЗАЦИЯ МАТРИЦЫ РАССТОЯНИЙ ===")
        print(Fore.CYAN + f"Размер матрицы: {n+1} строк (исходная: '{s}') x {m+1} столбцов (целевая: '{t}')")
        print(Fore.CYAN + "Исходная матрица:")
        print(Fore.CYAN + "   " + " ".join(f"{j:2}" for j in range(m+1)))
        for i, row in enumerate(dp):
            prefix = f"{i:2}:" if i > 0 else " 0:"
            print(Fore.CYAN + prefix + " ".join(f"{cell:2}" for cell in row))
        print()

    # Инициализация базового случая: преобразование пустой строки в префикс
    if verbose:
        print(Fore.YELLOW + "=== ИНИЦИАЛИЗАЦИЯ БАЗОВЫХ СЛУЧАЕВ ===")
        print(Fore.GREEN + "Заполнение первого столбца (удаление всех символов из исходной строки):")
    
    for i in range(1, n + 1):
        cost = deletion_cost(s[i - 1])
        dp[i][0] = dp[i - 1][0] + cost
        if verbose:
            symbol = s[i-1]
            special_note = f" (особый символ, стоимость={special_deletion_cost})" if symbol == special_deletion_symbol else ""
            print(Fore.GREEN + f"  dp[{i}][0] = dp[{i-1}][0] + deletion_cost('{symbol}'){special_note} = {dp[i-1][0]} + {cost} = {dp[i][0]}")

    if verbose:
        print(Fore.GREEN + "\nЗаполнение первой строки (вставка всех символов в пустую строку):")
    
    for j in range(1, m + 1):
        dp[0][j] = dp[0][j - 1] + 1  # стоимость вставки всегда 1
        if verbose:
            symbol = t[j-1]
            print(Fore.GREEN + f"  dp[0][{j}] = dp[0][{j-1}] + 1 (вставка '{symbol}') = {dp[0][j-1]} + 1 = {dp[0][j]}")
    
    if verbose:
        print(Fore.YELLOW + "\n=== МАТРИЦА ПОСЛЕ ИНИЦИАЛИЗАЦИИ ===")
        print(Fore.CYAN + "   " + " ".join(f"{j:2}" for j in range(m+1)))
        for i, row in enumerate(dp):
            prefix = f"{i:2}:" if i > 0 else " 0:"
            print(Fore.CYAN + prefix + " ".join(f"{cell:2}" for cell in row))
        print()

    # Заполнение матрицы dp
    if verbose:
        print(Fore.YELLOW + "=== ЗАПОЛНЕНИЕ МАТРИЦЫ ===")
    
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            cost_del = dp[i - 1][j] + deletion_cost(s[i - 1])
            cost_ins = dp[i][j - 1] + 1  # вставка
            cost_sub = dp[i - 1][j - 1] + substitution_cost(s[i - 1], t[j - 1])
            
            if verbose:
                print(Fore.MAGENTA + f"\nЯчейка dp[{i}][{j}] (символы: '{s[i-1]}' -> '{t[j-1]}'):")
                # Детализация удаления
                symbol = s[i-1]
                del_cost = deletion_cost(symbol)
                del_note = f" (особый символ, стоимость={special_deletion_cost})" if symbol == special_deletion_symbol else ""
                print(Fore.GREEN + f"  Удаление '{symbol}': dp[{i-1}][{j}] + {del_cost}{del_note} = {dp[i-1][j]} + {del_cost} = {cost_del}")
                
                # Детализация вставки
                symbol = t[j-1]
                print(Fore.GREEN + f"  Вставка '{symbol}': dp[{i}][{j-1}] + 1 = {dp[i][j-1]} + 1 = {cost_ins}")
                
                # Детализация замены
                source_symbol = s[i-1]
                target_symbol = t[j-1]
                sub_cost = substitution_cost(source_symbol, target_symbol)
                if source_symbol == target_symbol:
                    sub_note = " (символы одинаковые, стоимость=0)"
                elif target_symbol == special_replacer:
                    sub_note = f" (специальная замена, стоимость={special_replace_cost})"
                else:
                    sub_note = " (стандартная замена, стоимость=1)"
                print(Fore.GREEN + f"  Замена '{source_symbol}'->'{target_symbol}': dp[{i-1}][{j-1}] + {sub_cost}{sub_note} = {dp[i-1][j-1]} + {sub_cost} = {cost_sub}")
                
            dp[i][j] = min(cost_del, cost_ins, cost_sub)
            if verbose:
                print(Fore.BLUE + f"  ИТОГО: dp[{i}][{j}] = min({cost_del}, {cost_ins}, {cost_sub}) = {dp[i][j]}")
    
    if verbose:
        print(Fore.YELLOW + "\n=== ФИНАЛЬНАЯ МАТРИЦА ===")
        print(Fore.CYAN + "   " + " ".join(f"{j:2}" for j in range(m+1)))
        for i, row in enumerate(dp):
            prefix = f"{i:2}:" if i > 0 else " 0:"
            print(Fore.CYAN + prefix + " ".join(f"{cell:2}" for cell in row))
        print()

    return dp[n][m]


if __name__ == '__main__':
    import sys

    # Чтение входных данных
    input_lines = sys.stdin.read().splitlines()
    if len(input_lines) < 4:
        print(Fore.RED + "ОШИБКА: Недостаточно входных данных! Ожидается 4 строки:")
        print(Fore.RED + "  1. Исходная строка")
        print(Fore.RED + "  2. Целевая строка")
        print(Fore.RED + "  3. Специальный заменитель и его стоимость (например: '? 0')")
        print(Fore.RED + "  4. Особо удаляемый символ и его стоимость (например: '# 0')")
        sys.exit(1)

    s = input_lines[0].strip()
    t = input_lines[1].strip()

    # Обработка параметров специального заменителя: символ и его стоимость замены
    try:
        special_replacer, special_replace_cost = input_lines[2].split()
        special_replace_cost = int(special_replace_cost)
    except (IndexError, ValueError):
        print(Fore.RED + "ОШИБКА: Неверный формат данных для специального заменителя.")
        print(Fore.RED + "  Ожидается: символ и число (например: '? 0')")
        sys.exit(1)

    # Обработка параметров особо удаляемого символа: символ и его стоимость удаления
    try:
        special_deletion_symbol, special_deletion_cost = input_lines[3].split()
        special_deletion_cost = int(special_deletion_cost)
    except (IndexError, ValueError):
        print(Fore.RED + "ОШИБКА: Неверный формат данных для особо удаляемого символа.")
        print(Fore.RED + "  Ожидается: символ и число (например: '# 0')")
        sys.exit(1)

    # Чтение флага verbose
    verbose = True



    # Вычисление результата
    result = levenshtein_distance(
        s, t, special_replacer, special_replace_cost, special_deletion_symbol, special_deletion_cost, verbose
    )
    print(Fore.GREEN + Style.BRIGHT + f"\nРЕЗУЛЬТАТ: Расстояние Левенштейна = {result}")
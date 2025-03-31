def main():
    import sys
    from colorama import Fore, Style
    from levenshtein_calculator import LevenshteinCalculator  # Предполагается, что этот класс существует

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

    try:
        special_replacer, special_replace_cost_str = input_lines[2].split()
        special_replace_cost = float(special_replace_cost_str)
    except (IndexError, ValueError):
        print(Fore.RED + "ОШИБКА: Неверный формат данных для специального заменителя.")
        print(Fore.RED + "  Ожидается: символ и число (например: '? 0' или '? 0.5')")
        sys.exit(1)

    try:
        special_deletion_symbol, special_deletion_cost_str = input_lines[3].split()
        special_deletion_cost = float(special_deletion_cost_str)
    except (IndexError, ValueError):
        print(Fore.RED + "ОШИБКА: Неверный формат данных для особо удаляемого символа.")
        print(Fore.RED + "  Ожидается: символ и число (например: '# 0' или '# 0.5')")
        sys.exit(1)

    verbose = True

    calculator = LevenshteinCalculator(
        special_replacer,
        special_replace_cost,
        special_deletion_symbol,
        special_deletion_cost
    )

    result = calculator.calculate(s, t, verbose)
    print(Fore.GREEN + Style.BRIGHT + f"\nРЕЗУЛЬТАТ: Расстояние Левенштейна = {result}")


if __name__ == '__main__':
    main()
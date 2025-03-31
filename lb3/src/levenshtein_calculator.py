from typing import List, Tuple, Optional
from colorama import init, Fore, Back, Style

init(autoreset=True)

class LevenshteinCalculator:
    def __init__(self, 
                 special_replacer: str = '*', 
                 special_replace_cost: float = 0.5, 
                 special_deletion_symbol: str = '#', 
                 special_deletion_cost: float = 0.5):
        self.special_replacer = special_replacer
        self.special_replace_cost = special_replace_cost
        self.special_deletion_symbol = special_deletion_symbol
        self.special_deletion_cost = special_deletion_cost
        
    def _round_cost(self, cost: float) -> float:
        """Округляет стоимость до 2 знаков после запятой."""
        return round(cost, 2)


    def _deletion_cost(self, ch: str) -> float:
        """Функция стоимости удаления."""
        return self.special_deletion_cost if ch == self.special_deletion_symbol else 1.0

    def _substitution_cost(self, a: str, b: str) -> float:
        """Функция стоимости замены."""
        if a == b:
            return 0.0
        return self.special_replace_cost if b == self.special_replacer else 1.0

    def _initialize_matrices(self, n: int, m: int) -> Tuple[List[List[float]], List[List[str]]]:
        """
        Инициализация матриц с предварительным выделением памяти.
        Используется float для поддержки дробных стоимостей.
        """
        dp = [[0.0] * (m + 1) for _ in range(n + 1)]
        ops = [[""] * (m + 1) for _ in range(n + 1)]
        return dp, ops

    def _print_matrix(self, matrix: List[List[float]], title: str) -> None:
        """Вывод матрицы с форматированием."""
        print(Fore.YELLOW + f"\n=== {title} ===")
        if not matrix:
            print("Empty matrix")
            return
        
        header = "   " + " ".join(f"{j:>5}" for j in range(len(matrix[0])))
        print(Fore.CYAN + header)
        
        for i, row in enumerate(matrix):
            prefix = f"{i:>2}:" if i > 0 else "  0:"
            print(Fore.CYAN + prefix + " ".join(f"{cell:>5.1f}" if isinstance(cell, float) else f"{cell:>5}" for cell in row))

    def _fill_base_cases(self, 
                        dp: List[List[float]], 
                        ops: List[List[str]], 
                        s: str, 
                        t: str, 
                        verbose: bool) -> None:
        """Заполнение базовых случаев."""
        if verbose:
            print(Fore.YELLOW + "\n=== INITIALIZING BASE CASES ===")
            print(Fore.GREEN + "Filling first column (deleting all from source):")

        # Fill first column (deletions)
        for i in range(1, len(s) + 1):
            cost = self._deletion_cost(s[i-1])
            dp[i][0] = self._round_cost(dp[i-1][0] + cost)
            ops[i][0] = f"Del '{s[i-1]}'({cost})"
            if verbose:
                note = f" (special, cost={self.special_deletion_cost})" if s[i-1] == self.special_deletion_symbol else ""
                print(f"  dp[{i}][0] = {dp[i-1][0]} + {cost}{note} = {dp[i][0]}")

        if verbose:
            print(Fore.GREEN + "\nFilling first row (inserting all to empty string):")

        # Fill first row (insertions)
        for j in range(1, len(t) + 1):
            dp[0][j] = self._round_cost(dp[0][j-1] + 1.0)
            ops[0][j] = f"Ins '{t[j-1]}'(1)"
            if verbose:
                print(f"  dp[0][{j}] = {dp[0][j-1]} + 1 = {dp[0][j]}")
        if verbose:
            self._print_matrix(dp, "BASE MATRIX")

    def _fill_dp_matrix(self, 
                       dp: List[List[float]], 
                       ops: List[List[str]], 
                       s: str, 
                       t: str, 
                       verbose: bool) -> None:
        """Заполнение DP матрицы с минимизацией вычислений."""
        if verbose:
            print(Fore.YELLOW + "\n=== FILLING DP MATRIX ===")

        for i in range(1, len(s) + 1):
            for j in range(1, len(t) + 1):
                # Вычисляем все возможные стоимости
                del_cost = self._round_cost(dp[i-1][j] + self._deletion_cost(s[i-1]))
                ins_cost = self._round_cost(dp[i][j-1] + 1.0)
                sub_cost = self._round_cost(dp[i-1][j-1] + self._substitution_cost(s[i-1], t[j-1]))

                if verbose:
                    print(Fore.MAGENTA + f"\nCell [{i}][{j}] ('{s[i-1]}' → '{t[j-1]}'):")
                    print(f"  Del: {dp[i-1][j]} + {self._deletion_cost(s[i-1])} = {del_cost}")
                    print(f"  Ins: {dp[i][j-1]} + 1 = {ins_cost}")
                    print(f"  Sub: {dp[i-1][j-1]} + {self._substitution_cost(s[i-1], t[j-1])} = {sub_cost}")

                # Находим минимальную стоимость
                if sub_cost <= ins_cost and sub_cost <= del_cost:
                    dp[i][j] = sub_cost
                    if s[i-1] == t[j-1]:
                        ops[i][j] = f"Keep '{s[i-1]}'"
                    else:
                        cost = self._substitution_cost(s[i-1], t[j-1])
                        ops[i][j] = f"Sub '{s[i-1]}'→'{t[j-1]}'({cost})"
                elif ins_cost <= del_cost:
                    dp[i][j] = ins_cost
                    ops[i][j] = f"Ins '{t[j-1]}'(1)"
                else:
                    dp[i][j] = del_cost
                    ops[i][j] = f"Del '{s[i-1]}'({self._deletion_cost(s[i-1])})"

                if verbose:
                    print(Fore.BLUE + f"  RESULT: {dp[i][j]} - {ops[i][j]}")

    def _trace_operations(self, ops: List[List[str]], s: str, t: str, verbose: bool) -> None:
        """Восстановление последовательности операций."""
        if not verbose:
            return

        print(Fore.YELLOW + "\n=== OPERATION SEQUENCE ===")
        i, j = len(s), len(t)
        path = []
        
        while i > 0 or j > 0:
            op = ops[i][j]
            path.append(op)
            if "Sub" in op or "Keep" in op:
                i -= 1
                j -= 1
            elif "Ins" in op:
                j -= 1
            else:
                i -= 1
        
        for step, op in enumerate(reversed(path), 1):
            print(Fore.CYAN + f"{step}. {op}")

    def calculate(self, s: str, t: str, verbose: bool = False) -> float:
        """
        Расчет расстояния Левенштейна.
        Возвращает float для поддержки дробных стоимостей.
        """
        if not s and not t:
            return 0.0
            
        n, m = len(s), len(t)
        dp, ops = self._initialize_matrices(n, m)

        if verbose:
            print(Fore.YELLOW + f"\nComputing distance between: '{s}' and '{t}'")
            self._print_matrix(dp, "INITIAL MATRIX")

        self._fill_base_cases(dp, ops, s, t, verbose)
        self._fill_dp_matrix(dp, ops, s, t, verbose)

        if verbose:
            self._print_matrix(dp, "FINAL MATRIX")
            self._trace_operations(ops, s, t, verbose)

        return self._round_cost(dp[n][m])
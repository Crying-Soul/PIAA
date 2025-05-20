from operator import itemgetter
from collections import deque
from utils import *

class Node:
    def __init__(self, link=None, name="root", verbose=False):
        self.parent = None
        self.children = {}
        self.suffix_link = link
        self.terminal_link = None
        self.terminate = 0
        self.name = name
        self.verbose = verbose

    def __str__(self):
        parent_name = self.parent.name if self.parent else None
        suffix_name = self.suffix_link.name if self.suffix_link else None
        children_keys = list(self.children.keys()) if self.children else None
        return (
            f"Node(name={self.name}, "
            f"parent={parent_name}, "
            f"children={children_keys}, "
            f"suffix_link={suffix_name}, "
            f"terminate={self.terminate})"
        )

class AhoCorasickAutomaton:
    def __init__(self, patterns: dict, verbose=False):
        self.verbose = verbose
        if self.verbose:
            log_success("Дерево шаблонов инициализировано")
        self.root = Node(verbose=verbose)
        self.root.suffix_link = self.root  # важно!
        self.patterns = patterns
        self.patterns_inverse = {v: k for k, v in patterns.items()}
        self._build_automaton()
        if self.verbose:
            log_success("Автомат готов к поиску")

    def _build_automaton(self):
        self._build_trie()
        self._build_suffix_links()
        self._build_terminal_links()

    def _build_trie(self):
        if self.verbose:
            log_section("Построение дерева шаблонов")
        for pattern, pattern_id in self.patterns.items():
            if self.verbose:
                log_substep(f"Добавляем шаблон '{pattern}' (№{pattern_id})")
            current_node = self.root
            for symbol in pattern:
                if symbol not in current_node.children:
                    new_node = Node(name=symbol, link=self.root, verbose=self.verbose)
                    new_node.parent = current_node
                    current_node.children[symbol] = new_node
                    if self.verbose:
                        log_action(f"Создан узел '{symbol}'")
                    current_node = new_node
                else:
                    current_node = current_node.children[symbol]
                    if self.verbose:
                        log_info(f"Узел для '{symbol}' уже существует")
            current_node.terminate = pattern_id
            if self.verbose:
                log_result(f"Шаблон '{pattern}' помечен в узле {current_node.name}")

    def _build_suffix_links(self):
        if self.verbose:
            log_section("Построение суффиксных ссылок")

        queue = deque(self.root.children.values())

        # Устанавливаем суффиксные ссылки первого уровня
        for child in queue:
            child.suffix_link = self.root
            if self.verbose:
                log_info(
                    f"Узел '{child.name}' (прямой потомок корня): "
                    f"суффиксная ссылка → 'root'"
                )

        # Обход остальных узлов в ширину
        while queue:
            current_node = queue.popleft()
            for child_symbol, child_node in current_node.children.items():
                queue.append(child_node)

                if self.verbose:
                    log_substep(f"Обработка узла '{child_node.name}' по символу '{child_symbol}' (ребёнок '{current_node.name}')")

                # Ищем суффиксную ссылку
                fallback = current_node.suffix_link
                fallback_chain = [fallback.name]  # Для логирования цепочки

                while child_symbol not in fallback.children and fallback != self.root:
                    fallback = fallback.suffix_link
                    fallback_chain.append(fallback.name)

                if self.verbose:
                    log_info(
                        f"Цепочка fallback для символа '{child_symbol}': "
                        + " → ".join(fallback_chain)
                    )

                # Устанавливаем ссылку
                if child_symbol in fallback.children:
                    target = fallback.children[child_symbol]
                    child_node.suffix_link = target
                    if self.verbose:
                        log_result(
                            f"Суффиксная ссылка для узла '{child_node.name}' установлена → "
                            f"'{target.name}' (через '{fallback.name}')"
                        )
                else:
                    child_node.suffix_link = self.root
                    if self.verbose:
                        log_result(
                            f"Суффиксная ссылка для узла '{child_node.name}' установлена → "
                            f"'root' (символ '{child_symbol}' не найден в предках)"
                        )

    def _build_terminal_links(self):
        if self.verbose:
            log_section("Построение терминальных ссылок")
        queue = deque(self.root.children.values())
        while queue:
            current_node = queue.popleft()
            queue.extend(current_node.children.values())

            temp = current_node.suffix_link
            while temp != self.root:
                if temp.terminate:
                    current_node.terminal_link = temp
                    if self.verbose:
                        log_result(f"Термин. ссылка для '{current_node.name}' → '{temp.name}'")
                    break
                temp = temp.suffix_link

    def search_patterns(self, text: str) -> list[str]:
        if self.verbose:
            log_section(f"Поиск по тексту: {text}")
        results = []
        current_node = self.root

        for position, symbol in enumerate(text):
            if self.verbose:
                log_substep(f"Символ '{symbol}' (i={position})")

            while symbol not in current_node.children and current_node != self.root:
                if self.verbose:
                    log_info(f"'{symbol}' нет в '{current_node.name}', следуем по суфф. ссылке")
                current_node = current_node.suffix_link

            current_node = current_node.children.get(symbol, self.root)
            if self.verbose:
                log_info(f"Переход в узел: {current_node.name}")

            temp_node = current_node
            while temp_node:
                if temp_node.terminate:
                    pattern = self.patterns_inverse[temp_node.terminate]
                    start_pos = position - len(pattern) + 2  
                    results.append([start_pos, temp_node.terminate])
                    if self.verbose:
                        log_success(
                            f"[ПОИСК] Шаблон '{pattern}' найден в позиции {start_pos} "
                            f"(узел: '{temp_node.name}')"
                        )
                temp_node = temp_node.terminal_link

        results.sort(key=itemgetter(0, 1))
        formatted = [' '.join(map(str, item)) for item in results]
        if self.verbose:
            log_result(f"Всего совпадений: {len(formatted)}")
        return formatted

def read_input(verbose=False):
    n = int(input())
    patterns = {}
    for pattern_id in range(1, n + 1):
        pattern = input().strip()
        patterns[pattern] = pattern_id
        if verbose:
            log_info(f"Добавлен шаблон №{pattern_id}: '{pattern}'")
    return patterns

def main():
    verbose = True
    text = input().strip()
    patterns = read_input(verbose)
    automaton = AhoCorasickAutomaton(patterns, verbose)
    results = automaton.search_patterns(text)

    if results:
        if verbose:
            log_section("Результаты поиска")
        print('\n'.join(results))
    else:
        log_warning("Совпадения не найдены")

if __name__ == "__main__":
    main()

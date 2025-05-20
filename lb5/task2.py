from collections import deque
from utils import *

class TrieNode:
    def __init__(self, parent=None, name="root", verbose=False):
        self.parent = parent
        self.children = {}
        self.suffix_link = None
        self.terminal_link = None
        self.terminate = []
        self.name = name
        self.depth = parent.depth + 1 if parent else 0
        self.verbose = verbose

    def __repr__(self):
        parent_name = self.parent.name if self.parent else None
        suffix_name = self.suffix_link.name if self.suffix_link else None
        children_keys = list(self.children.keys()) if self.children else None
        return (
            f"TrieNode(name={self.name}, parent={parent_name}, children={children_keys}, "
            f"suffix_link={suffix_name}, depth={self.depth}, terminate={self.terminate})"
        )

class Trie:
    def __init__(self, verbose=False):
        self.root = TrieNode(verbose=verbose)
        self.root.suffix_link = self.root  # важно!
        self.verbose = verbose
        if self.verbose:
            log_success("Дерево шаблонов инициализировано")

    def add_pattern(self, pattern, offsets):
        if self.verbose:
            log_substep(f"Добавление шаблона: '{pattern}' с оффсетами: {offsets}")
        node = self.root
        for symbol in pattern:
            if symbol not in node.children:
                if self.verbose:
                    log_action(f"Создание нового узла для символа: '{symbol}'")
                new_node = TrieNode(parent=node, name=symbol, verbose=self.verbose)
                node.children[symbol] = new_node
                node = new_node
            else:
                if self.verbose:
                    log_info(f"Используется существующий узел для символа: '{symbol}'")
                node = node.children[symbol]
        node.terminate = offsets
        if self.verbose:
            log_result(f"Шаблон '{pattern}' успешно добавлен. Терминальный узел: {node}")

class AhoCorasick:
    def __init__(self, patterns, verbose=False):
        self.verbose = verbose
        if self.verbose:
            log_section("Инициализация автомата Ахо-Корасика")
        self.trie = Trie(verbose=verbose)
        self.patterns = patterns
        self._build_trie()
        self._build_suffix_links()
        self._build_terminal_links()
        if self.verbose:
            log_success("Автомат готов к поиску")

    def _build_trie(self):
        if self.verbose:
            log_section("Построение дерева шаблонов")
        for pattern, offsets in self.patterns.items():
            if self.verbose:
                log_substep(f"Добавляем шаблон '{pattern}'")
            self.trie.add_pattern(pattern, offsets)

    def _build_suffix_links(self):
        if self.verbose:
            log_section("Построение суффиксных ссылок")
        root = self.trie.root
        queue = deque(root.children.values())

        # Устанавливаем суффиксные ссылки первого уровня
        for child in queue:
            child.suffix_link = root
            if self.verbose:
                log_info(
                    f"Узел '{child.name}' (прямой потомок корня): суффиксная ссылка → 'root'"
                )

        # Обход остальных узлов в ширину
        while queue:
            current = queue.popleft()
            for symbol, child in current.children.items():
                queue.append(child)
                if self.verbose:
                    log_substep(f"Обработка узла '{child.name}' по символу '{symbol}' (ребёнок '{current.name}')")

                # Поиск суффиксной ссылки
                fallback = current.suffix_link
                fallback_chain = [fallback.name]
                while symbol not in fallback.children and fallback != root:
                    fallback = fallback.suffix_link
                    fallback_chain.append(fallback.name)
                if self.verbose:
                    log_info(f"Цепочка fallback для '{symbol}': {' → '.join(fallback_chain)}")

                if symbol in fallback.children:
                    target = fallback.children[symbol]
                    child.suffix_link = target
                    if self.verbose:
                        log_result(
                            f"Суффиксная ссылка для узла '{child.name}' установлена → '{target.name}' "
                            f"(через '{fallback.name}')"
                        )
                else:
                    child.suffix_link = root
                    if self.verbose:
                        log_result(
                            f"Суффиксная ссылка для узла '{child.name}' установлена → 'root' "
                            f"(символ '{symbol}' не найден в предках)"
                        )

    def _build_terminal_links(self):
        if self.verbose:
            log_section("Построение терминальных ссылок")
        root = self.trie.root
        queue = deque(root.children.values())
        while queue:
            current = queue.popleft()
            queue.extend(current.children.values())
            temp = current.suffix_link
            while temp != root:
                if temp.terminate:
                    current.terminal_link = temp
                    if self.verbose:
                        log_result(f"Термин. ссылка для '{current.name}' → '{temp.name}'")
                    break
                temp = temp.suffix_link

    def search(self, text, pattern_input, joker):
        if self.verbose:
            log_section(f"Поиск по тексту: {text}")
        result = [0] * len(text)
        node = self.trie.root

        for index, symbol in enumerate(text):
            if self.verbose:
                log_substep(f"Символ '{symbol}' (i={index})")

            while symbol not in node.children and node != self.trie.root:
                if self.verbose:
                    log_info(f"'{symbol}' нет в '{node.name}', следуем по суфф. ссылке")
                node = node.suffix_link

            node = node.children.get(symbol, self.trie.root)
            if self.verbose:
                log_info(f"Переход в узел: {node.name}")

            temp = node
            while temp:
                if temp.terminate:
                    matched = text[index - temp.depth + 1: index + 1]
                    for offset in self.patterns[matched]:
                        pos = index - temp.depth - offset + 1
                        if pos >= 0:
                            result[pos] += 1
                            if self.verbose:
                                log_success(
                                    f"[ПОИСК] Подшаблон '{matched}' найден в позиции {pos+1} (узел: '{temp.name}')"
                                )
                temp = temp.terminal_link

        # Формируем выходной результат
        output = []
        total_patterns = sum(len(v) for v in self.patterns.values())
        for i in range(len(result) - len(pattern_input) + 1):
            if result[i] == total_patterns:
                valid = True
                for j in range(len(pattern_input)):
                    if pattern_input[j] == joker and text[i + j] == joker:
                        valid = False
                        break
                if valid:
                    output.append(i + 1)
        if self.verbose:
            log_result(f"Всего совпадений: {len(output)}")
        return [str(pos) for pos in output]


def get_pattern_parts(pattern, joker, verbose=False):
    if verbose:
        log_section("Разделение шаблона по джокеру")
    parts = {}
    last_j = -1

    for i, char in enumerate(pattern):
        if char == joker:
            if last_j < i - 1:
                sub = pattern[last_j + 1: i]
                parts.setdefault(sub, []).append(last_j + 1)
                if verbose:
                    log_action(f"Найден подшаблон: '{sub}' (оффсет: {last_j + 1})")
            last_j = i

    if last_j != len(pattern) - 1:
        sub = pattern[last_j + 1:]
        parts.setdefault(sub, []).append(last_j + 1)
        if verbose:
            log_action(f"Найден подшаблон: '{sub}' (оффсет: {last_j + 1})")

    if verbose:
        log_success(f"Итоговые подшаблоны: {parts}")
    return parts


def main():
    verbose = True
    text = input().strip()
    pattern_input = input().strip()
    joker = input().strip()

    patterns = get_pattern_parts(pattern_input, joker, verbose)

    if not patterns:
        log_warning("Не найдено ни одного подшаблона")
        return

    automaton = AhoCorasick(patterns, verbose)
    result = automaton.search(text, pattern_input, joker)

    if result:
        if verbose:
            log_section("Результаты поиска")
        print('\n'.join(result))
    else:
        log_warning("Шаблон не найден в тексте")

if __name__ == "__main__":
    main()

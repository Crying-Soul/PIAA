from collections import deque
from utils import *

# === Структуры ===
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
        return f"TrieNode(name='{self.name}', depth={self.depth}, terminate={self.terminate})"


class Trie:
    def __init__(self, verbose=False):
        self.root = TrieNode(verbose=verbose)
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
                node.children[symbol] = TrieNode(parent=node, name=symbol, verbose=self.verbose)
            else:
                if self.verbose:
                    log_action(f"Используется существующий узел для символа: '{symbol}'")
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
            log_success("Построение автомата завершено")

    def _build_trie(self):
        if self.verbose:
            log_section("Построение дерева шаблонов")
        for pattern, offsets in self.patterns.items():
            self.trie.add_pattern(pattern, offsets)

    def _build_suffix_links(self):
        if self.verbose:
            log_section("Построение суффиксных ссылок")
        root = self.trie.root
        queue = deque(root.children.values())

        for child in queue:
            child.suffix_link = root
            if self.verbose:
                log_info(f"Суффиксная ссылка для '{child.name}' установлена на корень")

        while queue:
            current = queue.popleft()
            if self.verbose:
                log_substep(f"Обработка узла: '{current.name}' (глубина: {current.depth})")

            for symbol, child in current.children.items():
                queue.append(child)
                if self.verbose:
                    log_action(f"Потомок '{child.name}' добавлен в очередь")

                link = current.suffix_link
                while link is not None and symbol not in link.children:
                    if self.verbose:
                        log_info(f"Символ '{symbol}' не найден в '{link.name}', переход по ссылке")
                    link = link.suffix_link

                if link and symbol in link.children:
                    child.suffix_link = link.children[symbol]
                    if self.verbose:
                        log_result(f"Суффиксная ссылка для '{child.name}' установлена на '{child.suffix_link.name}'")
                else:
                    child.suffix_link = root
                    if self.verbose:
                        log_result(f"Суффиксная ссылка для '{child.name}' установлена на корень")

    def _build_terminal_links(self):
        if self.verbose:
            log_section("Построение терминальных ссылок")
        root = self.trie.root
        queue = deque(root.children.values())

        while queue:
            current = queue.popleft()
            if self.verbose:
                log_substep(f"Обработка узла: '{current.name}'")

            queue.extend(current.children.values())

            temp = current.suffix_link
            while temp and temp != root:
                if temp.terminate:
                    current.terminal_link = temp
                    if self.verbose:
                        log_result(f"Терминальная ссылка для '{current.name}' установлена на '{temp.name}'")
                    break
                temp = temp.suffix_link

    def search(self, text, pattern_input, joker):
        if self.verbose:
            log_section("Поиск по тексту")
        result = [0] * len(text)
        node = self.trie.root

        for index, symbol in enumerate(text):
            if self.verbose:
                log_substep(f"Символ '{symbol}' на позиции {index + 1}")
            while node and symbol not in node.children:
                node = node.suffix_link

            if node:
                node = node.children.get(symbol, self.trie.root)
            else:
                node = self.trie.root

            temp = node
            while temp:
                if temp.terminate:
                    matched = text[index - temp.depth + 1: index + 1]
                    for offset in self.patterns[matched]:
                        pos = index - temp.depth - offset + 1
                        if pos >= 0:
                            result[pos] += 1
                temp = temp.terminal_link

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
                    output.append(str(i + 1))

        return output


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
            log_section("Результаты")
        print('\n'.join(result))
    else:
        log_warning("Шаблон не найден в тексте")


if __name__ == "__main__":
    main()
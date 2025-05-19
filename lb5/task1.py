from operator import itemgetter
from collections import deque
from utils import * 

class Node:
    def __init__(self, link=None, name="root", verbose=False):
        self.parent = None
        self.children = {}
        self.suffix_link = link
        self.terminal_link = None
        self.terminate = 0  # Номер шаблона, если узел терминальный
        self.name = name    # Имя узла (символ или "root")
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
        self.patterns = patterns
        self.patterns_inverse = {v: k for k, v in patterns.items()}
        self._build_automaton()
        if self.verbose:
            log_success("Автомат готов к поиску")

    def _build_automaton(self):
        """Построение автомата Ахо-Корасик в три этапа"""
        self._build_trie()
        self._build_suffix_links()
        self._build_terminal_links()

    def _build_trie(self):
        """Построение исходного бора"""
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
        """Построение суффиксных ссылок в ширину (BFS)"""
        if self.verbose:
            log_section("Построение суффиксных ссылок")
        queue = deque(self.root.children.values())
        
        # Для детей корня суффиксная ссылка ведет в корень
        for child in queue:
            child.suffix_link = self.root
            if self.verbose:
                log_info(f"Суфф. ссылка для '{child.name}' → корень")

        while queue:
            current_node = queue.popleft()
            if self.verbose:
                log_substep(f"Обработка узла '{current_node.name}'")
            
            for child in current_node.children.values():
                queue.append(child)
                if self.verbose:
                    log_action(f"Добавлен в очередь '{child.name}'")
                self._set_suffix_link_for_child(child)
                if self.verbose:
                    log_result(f"Суфф. ссылка для '{child.name}' → '{child.suffix_link.name}'")

    def _set_suffix_link_for_child(self, node):
        """Установка суффиксной ссылки для конкретного узла"""
        link = node.parent.suffix_link

        while link and (node.name not in link.children):
            link = link.suffix_link

        if link:
            node.suffix_link = link.children.get(node.name, self.root)
        else:
            node.suffix_link = self.root

    def _build_terminal_links(self):
        """Построение терминальных ссылок в ширину (BFS)"""
        if self.verbose:
            log_section("Построение терминальных ссылок")
        queue = deque(self.root.children.values())

        while queue:
            current_node = queue.popleft()
            if self.verbose:
                log_substep(f"Узел '{current_node.name}'")
            
            # Добавляем детей текущего узла в очередь
            queue.extend(current_node.children.values())
            
            # Ищем ближайшую терминальную вершину по суффиксным ссылкам
            temp = current_node.suffix_link
            while temp != self.root:
                if temp.terminate:
                    current_node.terminal_link = temp
                    if self.verbose:
                        log_result(f"Термин. ссылка для '{current_node.name}' → '{temp.name}'")
                    break
                temp = temp.suffix_link

    def search_patterns(self, text: str) -> list[str]:
        """Поиск всех вхождений шаблонов в тексте"""
        if self.verbose:
            log_section("Поиск по тексту")
        results = []
        current_node = self.root

        for position, symbol in enumerate(text):
            if self.verbose:
                log_substep(f"Символ '{symbol}' (i={position})")
            
            # Переходим по суффиксным ссылкам, пока не найдем подходящего ребенка
            while current_node and symbol not in current_node.children:
                if self.verbose:
                    log_info(f"'{symbol}' нет в '{current_node.name}', следуем по суфф. ссылке")
                current_node = current_node.suffix_link

            if current_node:
                current_node = current_node.children.get(symbol, self.root)
                temp_node = current_node
                
                # Проверяем терминальные узлы по терминальным ссылкам
                while temp_node:
                    if temp_node.terminate:
                        pattern = self.patterns_inverse[temp_node.terminate]
                        start_pos = position - len(pattern) + 2  # +2 для 1-based индексации
                        results.append([start_pos, temp_node.terminate])
                        if self.verbose:
                            log_success(f"Найден шаблон '{pattern}' в позиции {start_pos}")
                    temp_node = temp_node.terminal_link
            else:
                current_node = self.root

        # Сортируем результаты и форматируем вывод
        results.sort(key=itemgetter(0, 1))
        formatted = [' '.join(map(str, item)) for item in results]
        if self.verbose:
            log_result(f"Всего совпадений: {len(formatted)}")
        return formatted


def read_input(verbose=False):
    """Чтение входных данных"""
    n = int(input())
    patterns = {}
    
    for pattern_id in range(1, n+1):
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
from graphviz import Digraph

class Visualizer:
    def __init__(self, automaton):
        self.automaton = automaton
        self.graph = Digraph(format='png')
        self.graph.attr('node', shape='circle', fontsize='10')
        self.graph.attr(rankdir='LR') 

    def _add_nodes(self, node, visited):
        # Label includes name and terminate flag
        label = f"{node.name}"
        if node.terminate:
            label += f"\\n(term={node.terminate})"
        self.graph.node(str(id(node)), label)
        visited.add(node)
        for child in node.children.values():
            if child not in visited:
                self._add_nodes(child, visited)

    def _add_trie_edges(self, node, visited):
        visited.add(node)
        for symbol, child in node.children.items():
            self.graph.edge(str(id(node)), str(id(child)), label=symbol)
            if child not in visited:
                self._add_trie_edges(child, visited)

    def _add_suffix_edges(self, node, visited):
        visited.add(node)
        if node is not self.automaton.root:
            target = node.suffix_link
            self.graph.edge(
                str(id(node)), str(id(target)),
                label='suffix', style='dashed', color='red'
            )
        for child in node.children.values():
            if child not in visited:
                self._add_suffix_edges(child, visited)

    def _add_terminal_edges(self, node, visited):
        visited.add(node)
        if node.terminal_link:
            target = node.terminal_link
            self.graph.edge(
                str(id(node)), str(id(target)),
                label='term', style='dotted', color='blue'
            )
        for child in node.children.values():
            if child not in visited:
                self._add_terminal_edges(child, visited)

    def render(self, filename='aho_automaton'):
        # Build graph
        self._add_nodes(self.automaton.root, set())
        self._add_trie_edges(self.automaton.root, set())
        self._add_suffix_edges(self.automaton.root, set())
        self._add_terminal_edges(self.automaton.root, set())
        
        # Render to file
        self.graph.render(filename, view=True)


from task1 import AhoCorasickAutomaton
patterns = {'her':1, 'she':2, 'his':3, 'is':4, 'i':5, 'he':6}
automaton = AhoCorasickAutomaton(patterns, verbose=False)
vis = Visualizer(automaton)
vis.render('aho_visualization')

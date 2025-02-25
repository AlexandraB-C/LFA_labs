import random
import matplotlib.pyplot as plt
import networkx as nx

class Grammar:
    def __init__(self, vn, vt, p, s):
        self.vn = vn
        self.vt = vt
        self.p = p
        self.s = s
        
    def gen_str(self, max_iter=50):
        curr = self.s
        i = 0
        
        while i < max_iter:
            # check no more nonterminals
            if all(sym not in self.vn for sym in curr):
                return curr
                
            possible_positions = []
            for idx, sym in enumerate(curr):
                if sym in self.vn:
                    possible_positions.append((idx, sym))
            
            if not possible_positions:
                break
                
            pos, sym = random.choice(possible_positions)
            possible_rules = [rule[1] for rule in self.p if rule[0] == sym]
            if not possible_rules:
                break
                
            new_str = random.choice(possible_rules)
            curr = curr[:pos] + new_str + curr[pos + 1:]
            i += 1
        
        return curr if all(sym not in self.vn for sym in curr) else None

    def gen_mult_strs(self, cnt=5):
        strs = set()
        tries = 0
        max_tries = cnt * 20
        
        while len(strs) < cnt and tries < max_tries:
            if res := self.gen_str():
                if all(c in self.vt for c in res):
                    strs.add(res)
            tries += 1
            
        return list(strs)

    def to_fa(self):
        # convert
        states = self.vn | {'F'}
        alpha = self.vt
        trans = {}
        init = self.s
        final = {'F'}

        for state in states:
            trans[state] = {}

        # gotta make them transition fam
        for state in self.vn:
            for rule in self.p:
                if rule[0] == state:
                    if rule[1] == 'e':
                        # empty string prod
                        final.add(state)
                    elif len(rule[1]) == 1 and rule[1] in self.vt:
                        # terminal prod
                        if rule[1] not in trans[state]:
                            trans[state][rule[1]] = set()
                        trans[state][rule[1]].add('F')
                    elif len(rule[1]) >= 2:
                        # handle longer prod
                        first_char = rule[1][0]
                        if first_char in self.vt:
                            next_state = rule[1][1] if len(rule[1]) > 1 else 'F'
                            if first_char not in trans[state]:
                                trans[state][first_char] = set()
                            trans[state][first_char].add(next_state)

        return FA(states, alpha, trans, init, final)
    
    def classify_chomsky(self):
        # classifying based on chomsky hierarchy
        # type 0: unrestricted
        # type 1: context-sensitive
        # type 2: context-free
        # type 3: regular
        
        is_type3 = True
        is_type2 = True
        is_type1 = True
        
        for lhs, rhs in self.p:
            # check if it's type 3 (regular)
            # either A → a or A → aB where A,B ∈ Vn and a ∈ Vt
            if lhs in self.vn:
                if len(rhs) == 0:
                    is_type3 = False
                elif len(rhs) == 1 and rhs in self.vt:
                    # A → a, this is fine for type 3
                    pass
                elif len(rhs) == 2 and rhs[0] in self.vt and rhs[1] in self.vn:
                    # A → aB, this is fine for type 3
                    pass
                elif rhs == 'e':  # epsilon is allowed in regular grammars
                    pass
                else:
                    is_type3 = False
            else:
                is_type3 = False
                is_type2 = False
                is_type1 = False
                break
            
            # check if it's type 2 (context-free)
            # all rules must be A → α where A ∈ Vn and α ∈ (Vn ∪ Vt)*
            if len(lhs) != 1 or lhs not in self.vn:
                is_type2 = False
                is_type1 = False
            
            # check if it's type 1 (context-sensitive)
            # all rules must be α → β where |α| <= |β| except S → ε
            if len(lhs) > len(rhs) and not (lhs == self.s and rhs == 'e'):
                is_type1 = False
        
        if is_type3:
            return "Type 3: Regular Grammar"
        elif is_type2:
            return "Type 2: Context-Free Grammar"
        elif is_type1:
            return "Type 1: Context-Sensitive Grammar"
        else:
            return "Type 0: Unrestricted Grammar"

class FA:
    def __init__(self, states, alpha, trans, init, final):
        self.states = states
        self.alpha = alpha
        self.trans = trans
        self.init = init
        self.final = final

    def check_str(self, inp):
        # check if input valid
        if not inp and self.init in self.final:
            return True
            
        curr_states = {self.init}
        
        for c in inp:
            if c not in self.alpha:
                return False
                
            next_states = set()
            for state in curr_states:
                if state in self.trans and c in self.trans[state]:
                    next_states.update(self.trans[state][c])
            
            if not next_states:
                return False
                
            curr_states = next_states

        return any(state in self.final for state in curr_states)
    
    def to_grammar(self):
        # convert FA to regular grammar
        vn = self.states - self.final  # non-terminals are states except finals
        vt = self.alpha  # terminals are alphabet
        p = []  # productions
        s = self.init  # start symbol is initial state
        
        # add rules based on transitions
        for state in self.states:
            for symbol in self.alpha:
                if symbol in self.trans.get(state, {}):
                    for next_state in self.trans[state][symbol]:
                        # if transition to final state, create rule state -> symbol
                        if next_state in self.final:
                            p.append((state, symbol))
                        # if transition to another state, create rule state -> symbol + next_state
                        else:
                            p.append((state, symbol + next_state))
                            
        # add epsilon rule for initial state if it's final
        if self.init in self.final:
            p.append((self.init, 'e'))
            
        return Grammar(vn, vt, p, s)
    
    def is_deterministic(self):
        # check if FA is deterministic
        for state in self.states:
            for symbol in self.alpha:
                if symbol in self.trans.get(state, {}):
                    # if there's more than one state for a symbol from this state, it's non-deterministic
                    if len(self.trans[state][symbol]) > 1:
                        return False
        return True
    
    def to_dfa(self):
        if self.is_deterministic():
            # already deterministic
            return self
        
        # we need to create a DFA from NDFA
        new_states = set()
        new_trans = {}
        new_final = set()
        
        # start with the epsilon closure of initial state
        initial_set = frozenset([self.init])
        states_queue = [initial_set]
        new_states.add(initial_set)
        
        # process all reachable state sets
        while states_queue:
            current_set = states_queue.pop(0)
            new_trans[current_set] = {}
            
            # if any state in the set is final, the new state is final
            if any(state in self.final for state in current_set):
                new_final.add(current_set)
            
            # for each symbol, find all possible next states
            for symbol in self.alpha:
                next_states = set()
                for state in current_set:
                    if state in self.trans and symbol in self.trans[state]:
                        next_states.update(self.trans[state][symbol])
                
                if next_states:
                    next_set = frozenset(next_states)
                    new_trans[current_set][symbol] = {next_set}
                    
                    if next_set not in new_states:
                        new_states.add(next_set)
                        states_queue.append(next_set)
        
        # map frozensets to state names for readability
        state_mapping = {state_set: f"q{''.join(sorted(state for state in state_set))}" for state_set in new_states}
        
        readable_states = {state_mapping[state_set] for state_set in new_states}
        readable_trans = {}
        
        for state_set in new_trans:
            readable_trans[state_mapping[state_set]] = {}
            for symbol in new_trans[state_set]:
                readable_trans[state_mapping[state_set]][symbol] = {state_mapping[next_set] for next_set in new_trans[state_set][symbol]}
        
        readable_init = state_mapping[initial_set]
        readable_final = {state_mapping[state_set] for state_set in new_final}
        
        return FA(readable_states, self.alpha, readable_trans, readable_init, readable_final)
    
    def visualize(self, filename="automaton"):
        # gonna use networkx and matplotlib instead of graphviz
        G = nx.DiGraph()
        
        # add nodes for all states
        for state in self.states:
            G.add_node(state)
        
        # add edges for transitions
        edge_labels = {}
        for src_state in self.trans:
            for symbol in self.trans[src_state]:
                for dest_state in self.trans[src_state][symbol]:
                    # add edge if not already there
                    if G.has_edge(src_state, dest_state):
                        # update label with new symbol
                        edge_labels[(src_state, dest_state)] += f", {symbol}"
                    else:
                        G.add_edge(src_state, dest_state)
                        edge_labels[(src_state, dest_state)] = symbol
        
        # create figure
        plt.figure(figsize=(10, 8))
        
        # draw graph with circular layout
        pos = nx.spring_layout(G)
        
        # draw nodes with different colors for initial and final states
        node_colors = []
        for node in G.nodes():
            if node == self.init and node in self.final:
                node_colors.append('purple')  # initial and final
            elif node == self.init:
                node_colors.append('green')   # initial only
            elif node in self.final:
                node_colors.append('red')     # final only
            else:
                node_colors.append('skyblue') # normal state
        
        # draw nodes
        nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=700)
        
        # draw edges
        nx.draw_networkx_edges(G, pos, arrowsize=20, arrowstyle='->', width=1.5)
        
        # draw edge labels
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10)
        
        # draw node labels
        nx.draw_networkx_labels(G, pos, font_size=12, font_weight='bold')
        
        # add legend for colors
        legend_elements = [
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='green', markersize=10, label='Initial State'),
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='red', markersize=10, label='Final State'),
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='purple', markersize=10, label='Initial & Final State'),
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='skyblue', markersize=10, label='Normal State')
        ]
        plt.legend(handles=legend_elements, loc='upper right')
        
        # remove axis
        plt.axis('off')
        
        # save and show
        plt.savefig(f"{filename}.png")
        print(f"Graph saved to {filename}.png")

def main():
    # testing original Grammar
    vn = {'S', 'L', 'D'}
    vt = {'a', 'b', 'c', 'd', 'e', 'f', 'j'}
    p = [
        ('S', 'aS'),
        ('S', 'bS'),
        ('S', 'cD'),
        ('S', 'dL'),
        ('S', 'e'),
        ('L', 'eL'),
        ('L', 'fL'),
        ('L', 'jD'),
        ('L', 'e'),
        ('D', 'eD'),
        ('D', 'd')
    ]
    s = 'S'

    g = Grammar(vn, vt, p, s)
    
    print("Original grammar classification:", g.classify_chomsky())
    
    # strings = g.gen_mult_strs(5)
    # for i, str in enumerate(strings, 1):
    #     print(f"{i}. {str}")
    
    # variant 4 finite automaton
    fa_states = {'q0', 'q1', 'q2', 'q3'}
    fa_alphabet = {'a', 'b'}
    fa_transitions = {
        'q0': {'a': {'q1', 'q2'}},
        'q1': {'b': {'q1'}, 'a': {'q2'}},
        'q2': {'a': {'q1'}, 'b': {'q3'}}
    }
    fa_initial = 'q0'
    fa_final = {'q3'}
    
    fa = FA(fa_states, fa_alphabet, fa_transitions, fa_initial, fa_final)
    
    # check if deterministic
    is_dfa = fa.is_deterministic()
    print(f"Is the FA deterministic? {is_dfa}")
    
    # convert to deterministic if needed
    if not is_dfa:
        print("Converting NDFA to DFA")
        dfa = fa.to_dfa()
        print("DFA states:", dfa.states)
        print("DFA transitions:", dfa.trans)
        print("DFA initial state:", dfa.init)
        print("DFA final states:", dfa.final)
    
    # convert FA to grammar
    rg = fa.to_grammar()
    print("Converted grammar productions:")
    for rule in rg.p:
        print(f"{rule[0]} -> {rule[1]}")
    
    print("Grammar classification:", rg.classify_chomsky())
    
    # visualize the automaton
    try:
        fa.visualize("variant4_ndfa")
        if not is_dfa:
            dfa.visualize("variant4_dfa")
    except Exception as e:
        print(f"Error visualizing: {e}")
        print("Note: matplotlib and networkx must be installed for visualization")

if __name__ == "__main__":
    main()
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

class Grammar:
    def __init__(self, vn, vt, p, s):
        self.VN = vn  # non-terms
        self.VT = vt  # terms
        self.P = p    # rules
        self.S = s    # start
    
    def classify_grammar(self):
        is_regular = True
        is_right_linear = True
        is_left_linear = True
        is_context_free = True
        is_context_sensitive = True

        for lhs, rhs_list in self.P.items():
            if len(lhs) != 2 or lhs not in self.VN:
                is_context_free = False
            
            for rhs in rhs_list:
                if rhs == "":
                    continue
                
                if len(rhs) > 2:
                    is_right_linear = False
                    is_left_linear = False
                elif len(rhs) == 2:
                    if rhs[0] in self.VN and rhs[1] in self.VT:
                        is_right_linear = False
                    if rhs[0] in self.VT and rhs[1] in self.VN:
                        is_left_linear = False
                    if rhs[0] in self.VN and rhs[1] in self.VN:
                        is_right_linear = False
                        is_left_linear = False
                elif len(rhs) == 1:
                    if rhs[0] in self.VN:
                        is_right_linear = False
                        is_left_linear = False
                    
                if len(lhs) > len(rhs):
                    is_context_sensitive = False
        
        if is_right_linear or is_left_linear:
            return "Type 3 (Regular Grammar)"
        elif is_context_free:
            return "Type 2 (Context-Free Grammar)"
        elif is_context_sensitive:
            return "Type 1 (Context-Sensitive Grammar)"
        else:
            return "Type 0 (Unrestricted Grammar)"


class FiniteAutomaton:
    def __init__(self, q, sigma, delta, q0, f):
        self.Q = q          # states
        self.Sigma = sigma  # alphabet
        self.Delta = delta  # transitions
        self.q0 = q0        # init state
        self.F = f          # final states
    
    def is_deterministic(self):
        for state in self.Q:
            if state not in self.Delta: continue
            
            for sym in self.Sigma:
                if sym not in self.Delta[state]: continue
                
                if len(self.Delta[state][sym]) > 1:
                    return False
        
        return True
    
    def to_regular_grammar(self):
        # fa to reg grammar
        vn = set(self.Q)
        vt = set(self.Sigma)
        p = {state: [] for state in self.Q}
        s = self.q0
        
        for state in self.Q:
            if state not in self.Delta: continue
            
            for sym in self.Sigma:
                if sym not in self.Delta[state]: continue
                
                for next_state in self.Delta[state][sym]:
                    # add A -> aB
                    p[state].append(sym + next_state)
        
        for state in self.F:
            p[state].append("")
        
        return Grammar(vn, vt, p, s)
    
    def to_dfa(self):
        # ndfa to dfa
        if self.is_deterministic(): return self
        
        # init dfa
        dfa_q = set()
        dfa_sigma = self.Sigma
        dfa_delta = {}
        dfa_q0 = frozenset([self.q0])
        dfa_f = set()
        
        queue = [dfa_q0]
        done = set()
        
        while queue:
            curr = queue.pop(0)
            
            if curr in done: continue
            
            done.add(curr)
            curr_name = self._state_name(curr)
            dfa_q.add(curr_name)
            
            # check if final
            for state in curr:
                if state in self.F:
                    dfa_f.add(curr_name)
                    break
            
            if curr_name not in dfa_delta:
                dfa_delta[curr_name] = {}
            
            for sym in self.Sigma:
                next_states = set()
                
                for state in curr:
                    if state in self.Delta and sym in self.Delta[state]:
                        next_states.update(self.Delta[state][sym])
                
                if next_states:
                    next_frozen = frozenset(next_states)
                    next_name = self._state_name(next_frozen)
                    
                    dfa_delta[curr_name][sym] = {next_name}
                    
                    if next_frozen not in done:
                        queue.append(next_frozen)
        
        return FiniteAutomaton(dfa_q, dfa_sigma, dfa_delta, self._state_name(dfa_q0), dfa_f)
    
    def _state_name(self, states):
        # name for composite state
        if not states: return "∅"
        return "{" + ",".join(sorted(states)) + "}"
    
    def visualize_matplotlib(self, title="FA"):
        G = nx.DiGraph()
        # add nodes
        G.add_nodes_from(self.Q)
        
        edge_labels = {}
        for state in self.Q:
            if state not in self.Delta: continue
                
            for sym in self.Sigma:
                if sym not in self.Delta[state]: continue
                    
                for next_state in self.Delta[state][sym]:
                    if (state, next_state) in edge_labels:
                        edge_labels[(state, next_state)] += f", {sym}"
                    else:
                        edge_labels[(state, next_state)] = sym
                        G.add_edge(state, next_state)
        
        plt.figure(figsize=(10, 8))
        plt.title(title)
        pos = nx.spring_layout(G, seed=42)
        reg_states = [s for s in self.Q if s not in self.F]
        nx.draw_networkx_nodes(G, pos, nodelist=reg_states, node_color='lightblue', 
                              node_size=700, alpha=0.8)
        
        # final states
        if self.F:
            for s in self.F:
                nx.draw_networkx_nodes(G, pos, nodelist=[s], node_color='lightgreen', 
                                     node_size=700, alpha=0.8)
                nx.draw_networkx_nodes(G, pos, nodelist=[s], node_color='white', 
                                     node_size=600, alpha=0.8)
        
        nx.draw_networkx_edges(G, pos, arrowsize=20, arrowstyle='->', connectionstyle='arc3,rad=0.1')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10)
        nx.draw_networkx_labels(G, pos, font_size=12, font_weight='bold')
        
        # initial
        x0, y0 = pos[self.q0]
        plt.annotate('', xy=(x0, y0), xytext=(x0-0.3, y0),
                   arrowprops=dict(arrowstyle='->', lw=2, color='black'))
        plt.text(x0-0.35, y0, '', fontsize=12)
        
        reg_patch = plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='lightblue', 
                             markersize=15, label='regular')
        final_patch = plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='lightgreen', 
                               markersize=15, label='final')
        plt.legend(handles=[reg_patch, final_patch], loc='best')
        
        plt.axis('off')
        plt.tight_layout()
        plt.show()
        
        return plt

def main():
    states = {"q0", "q1", "q2", "q3"}
    alphabet = {"a", "b"}
    transitions = {
        "q0": {"a": {"q1", "q2"}},
        "q1": {"b": {"q1"}, "a": {"q2"}},
        "q2": {"a": {"q1"}, "b": {"q3"}}
    }
    initial_state = "q0"
    final_states = {"q3"}
    
    fa = FiniteAutomaton(states, alphabet, transitions, initial_state, final_states)
    
    print("Q = {q0,q1,q2,q3},")
    print("∑ = {a,b},")
    print("F = {q3},")
    print("δ(q0,a) = q1,")
    print("δ(q0,a) = q2,")
    print("δ(q1,b) = q1,")
    print("δ(q1,a) = q2,")
    print("δ(q2,a) = q1,")
    print("δ(q2,b) = q3.")
    
    print("\ndeterministic?", fa.is_deterministic())
    
    reg_grammar = fa.to_regular_grammar()
    print("\nregular grammar equiv:")
    print(f"VN = {reg_grammar.VN}")
    print(f"VT = {reg_grammar.VT}")
    print("P = {")
    for lhs, rhs_list in reg_grammar.P.items():
        for rhs in rhs_list:
            print(f"    {lhs} → {rhs if rhs else 'ε'}")
    print("}")
    print(f"S = {reg_grammar.S}")
    
    print("\ngrammar type:", reg_grammar.classify_grammar())
    
    dfa = fa.to_dfa()
    print("\ndfa equiv:")
    print(f"Q = {dfa.Q}")
    print(f"∑ = {dfa.Sigma}")
    print(f"q0 = {dfa.q0}")
    print(f"F = {dfa.F}")
    print("δ = {")
    for state in dfa.Q:
        if state not in dfa.Delta: continue
        for sym in dfa.Sigma:
            if sym not in dfa.Delta[state]: continue
            for next_state in dfa.Delta[state][sym]:
                print(f"    δ({state}, {sym}) = {next_state}")
    print("}")
    
    # prev lab
    vn = {"S", "L", "D"}
    vt = {"a", "b", "c", "d", "e", "f", "j"}
    p = {
        "S": ["aS", "bS", "cD", "dL", "e"],
        "L": ["eL", "fL", "jD", "e"],
        "D": ["eD", "d"]
    }
    prev_grammar = Grammar(vn, vt, p, "S")
    print("\nprev grammar type:", prev_grammar.classify_grammar())
    
    fa.visualize_matplotlib("NDFA")
    dfa.visualize_matplotlib("DFA")

if __name__ == "__main__":
    main()
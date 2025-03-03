import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

class Grammar:
    def __init__(self, vn, vt, p, s):
        # init grammar
        self.VN = vn  # non-terms
        self.VT = vt  # terms
        self.P = p    # rules
        self.S = s    # start
    
    def classify_grammar(self):
        # check grammar type
        is_right = True
        is_left = True
        
        for lhs, rhs_list in self.P.items():
            for rhs in rhs_list:
                # empty ok for reg grammar
                if len(rhs) == 0: continue
                
                # check right-linear (A→aB or A→a)
                if len(rhs) > 2 or (len(rhs) == 2 and rhs[1] not in self.VN) or (len(rhs) == 1 and rhs[0] in self.VN):
                    is_right = False
                
                # check left-linear (A→Ba or A→a)
                if len(rhs) > 2 or (len(rhs) == 2 and rhs[0] not in self.VN) or (len(rhs) == 1 and rhs[0] in self.VN):
                    is_left = False
        
        if is_right or is_left:
            return "Type 3 (Regular Grammar)"
        
        # check type 2 (context-free)
        is_cf = True
        for lhs, rhs_list in self.P.items():
            if len(lhs) != 1 or lhs not in self.VN:
                is_cf = False
                break
        
        if is_cf:
            return "Type 2 (Context-Free Grammar)"
        
        # check type 1 (context-sensitive)
        is_cs = True
        for lhs, rhs_list in self.P.items():
            for rhs in rhs_list:
                # exception for S→ε
                if len(rhs) == 0 and lhs == self.S:
                    s_on_rhs = False
                    for _, prods in self.P.items():
                        for prod in prods:
                            if self.S in prod:
                                s_on_rhs = True
                                break
                        if s_on_rhs: break
                    if not s_on_rhs: continue
                
                if len(lhs) > len(rhs):
                    is_cs = False
                    break
            if not is_cs: break
        
        if is_cs:
            return "Type 1 (Context-Sensitive Grammar)"
        
        # else type 0
        return "Type 0 (Unrestricted Grammar)"


class FiniteAutomaton:
    def __init__(self, q, sigma, delta, q0, f):
        # init fa
        self.Q = q          # states
        self.Sigma = sigma  # alphabet
        self.Delta = delta  # transitions
        self.q0 = q0        # init state
        self.F = f          # final states
    
    def is_deterministic(self):
        # check if dfa
        for state in self.Q:
            if state not in self.Delta: continue
            
            for sym in self.Sigma:
                if sym not in self.Delta[state]: continue
                
                if len(self.Delta[state][sym]) > 1:
                    return False
        
        return True
    
    def to_regular_grammar(self):
        # fa → reg grammar
        vn = set(self.Q)
        vt = set(self.Sigma)
        p = {state: [] for state in self.Q}
        s = self.q0
        
        for state in self.Q:
            if state not in self.Delta: continue
            
            for sym in self.Sigma:
                if sym not in self.Delta[state]: continue
                
                for next_state in self.Delta[state][sym]:
                    # add A→aB
                    p[state].append(sym + next_state)
        
        # add A→ε for final states
        for state in self.F:
            p[state].append("")
        
        return Grammar(vn, vt, p, s)
    
    def to_dfa(self):
        # ndfa → dfa
        if self.is_deterministic(): return self
        
        # init dfa
        dfa_q = set()
        dfa_sigma = self.Sigma
        dfa_delta = {}
        dfa_q0 = frozenset([self.q0])
        dfa_f = set()
        
        # bfs queue
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
            
            # init transitions
            if curr_name not in dfa_delta:
                dfa_delta[curr_name] = {}
            
            # process each sym
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
        # viz with matplotlib
        G = nx.DiGraph()
        
        # add nodes
        G.add_nodes_from(self.Q)
        
        # add edges
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
        
        # create fig
        plt.figure(figsize=(10, 8))
        plt.title(title)
        
        # positions
        pos = nx.spring_layout(G, seed=42)
        
        # draw nodes
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
        
        # draw edges
        nx.draw_networkx_edges(G, pos, arrowsize=20, arrowstyle='->', connectionstyle='arc3,rad=0.1')
        
        # edge labels
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10)
        
        # node labels
        nx.draw_networkx_labels(G, pos, font_size=12, font_weight='bold')
        
        # mark initial
        x0, y0 = pos[self.q0]
        plt.annotate('', xy=(x0, y0), xytext=(x0-0.3, y0),
                   arrowprops=dict(arrowstyle='->', lw=2, color='black'))
        plt.text(x0-0.35, y0, 'start', fontsize=12)
        
        # legend
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
    # var from assignment
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
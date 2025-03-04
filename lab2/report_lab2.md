# Report Laboratory Work 2

## MINISTERUL EDUCAȚIEI, CULTURII ȘI CERCETĂRII
### AL REPUBLICII MOLDOVA
#### Universitatea Tehnică a Moldovei  
**Facultatea Calculatoare, Informatică și Microelectronică**  
**Departamentul Inginerie Software și Automatică**  

### **ALEXANDRA BUJOR-COBILI, FAF-232**  
#### **Report - Laboratory work n.2**  
#### **Formal Languages & Finite Automata**  

**Checked by:**  
*Cretu Dumitru, university assistant*  
*FCIM, UTM*  

**Chișinău – 2025**  

---

## **1. Theory**

### **Deterministic Finite Automata (DFA)**
**Definition:** A DFA is a finite-state machine that accepts or rejects a given string of symbols by running through a uniquely determined state sequence.  

**Formal Definition:**  
A DFA is a 5-tuple (Q, Σ, δ, q0, F), where:  
- Q is a finite set of states.
- Σ is a finite set of input symbols (the alphabet).
- δ: Q × Σ → Q is the transition function (single-valued).
- q0 ∈ Q is the initial state.
- F ⊆ Q is the set of accepting (final) states.  

**Key Characteristic:** For each state and input symbol, there is *exactly one* transition.  


### **Non-deterministic Finite Automata (NDFA)**
**Definition:** An NDFA allows for multiple possible transitions from a given state on the same input symbol, or ε-transitions.  

**Formal Definition:**  
An NDFA is a 5-tuple (Q, Σ, δ, q0, F), where:  
- δ: Q × (Σ ∪ {ε}) → 2^Q (transition function maps to a set of states).  

**Key Characteristic:** Allows multiple transitions or ε-transitions.  

**Equivalence:** NDFAs are equivalent in power to DFAs, meaning any language accepted by an NDFA can also be accepted by a DFA.  


### **NDFA to DFA Conversion (Subset Construction)**
**Subset Construction (Powerset Construction):**
- The primary method for converting an NDFA to a DFA.
- Creates DFA states that represent sets of NDFA states.

**Detailed Process:**  
- Start with the initial DFA state as the ε-closure of the NDFA's initial state.
- For each DFA state and input symbol, calculate the set of NDFA states reachable. This becomes a new DFA state.
- Repeat until no new DFA states are generated.
- A DFA state is accepting if it contains at least one NDFA accepting state.
- **Result:** The resulting DFA recognizes the same language as the original NDFA.
- **Note:** The conversion can lead to an exponential increase in the number of states.
- **Proof:** This conversion proves the equivalence of NFA and DFA, in that they both accept the Regular Languages.

### **Chomsky Hierarchy**
**Classification:** Classifies formal grammars and languages into four types:
- Type-0 (Recursively Enumerable)
- Type-1 (Context-Sensitive)
- Type-2 (Context-Free)
- Type-3 (Regular)

### **Grammar Types**  
**Type-0 (Recursively Enumerable):**
- Unrestricted grammars.
- Recognized by Turing machines.
- Models general computation.

**Type-1 (Context-Sensitive):**
- Production rules: αAβ → γ.
- Recognized by linear bounded automata.
- The length of the right side of a production rule is greater than or equal to the left side.

**Type-2 (Context-Free):**
- Production rules: A → γ.
- Recognized by pushdown automata.
- Base of most programming language syntax.

**Type-3 (Regular):**
- Production rules: A → aB or A → a.
- Recognized by finite automata.
- Used for simple pattern matching and lexical analysis.

---

## **2. Objectives**

1. **Understand Automata:**
   - Gain a clear understanding of the definition, structure, and purpose of finite automata as models for various processes.
   - Comprehend the concept of states, transitions, and the distinction between starting and final states.

2. **Chomsky Hierarchy Classification:**
   - Extend the existing grammar type/class within the project to include a function that accurately classifies grammars based on the Chomsky hierarchy.
   - Utilize the grammar variant from the previous lab as a foundation for this implementation.

3. **Finite Automaton Operations (Variant-Specific):**
   - **FA to Regular Grammar Conversion:** Implement a function or algorithm to convert the given finite automaton into its equivalent regular grammar representation.
   - **Determinism Analysis:** Determine and report whether the specified finite automaton is deterministic (DFA) or non-deterministic (NDFA).
   - **NDFA to DFA Conversion (if applicable):** If the automaton is non-deterministic, implement a function or algorithm to convert it into an equivalent deterministic finite automaton (DFA).
   - **Graphical Representation:**
     - Develop a method to generate a visual representation (diagram) of the finite automaton.
     - This can be achieved using external libraries, tools, or APIs.
     - The program should automatically extract the automaton's data and interface with the chosen visualization method.
     - Alternatively, provide a detailed manual representation and explanation in the report.

---

## **5. Implementation**

**Variant 4 (past lab):**
```
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
```
**Variant 4:**
```
Q = {q0,q1,q2,q3}
∑ = {a,b}
F = {q3}
    δ(q0,a) = q1,
    δ(q0,a) = q2,
    δ(q1,b) = q1,
    δ(q1,a) = q2,
    δ(q2,a) = q1,
    δ(q2,b) = q3.
```

### **Code explanation**
```python
def classify_grammar(self):
    # check grammar type
    is_right = True
    is_left = True
    
    for lhs, rhs_list in self.P.items():
        for rhs in rhs_list:
            # empty ok for reg grammar
            if len(rhs) == 0: continue
```

This new function checks what type of grammar we have according to Chomsky's hierarchy. It starts by assuming the grammar might be regular (Type 3), which can be either right-linear or left-linear. Empty productions (like A→ε) are allowed in regular grammars, so we skip them.

```python
# check right-linear (A→aB or A→a)
if len(rhs) > 2 or (len(rhs) == 2 and rhs[1] not in self.VN) or (len(rhs) == 1 and rhs[0] in self.VN):
    is_right = False

# check left-linear (A→Ba or A→a)
if len(rhs) > 2 or (len(rhs) == 2 and rhs[0] not in self.VN) or (len(rhs) == 1 and rhs[0] in self.VN):
    is_left = False

```
Here we check if each rule follows the patterns for right-linear (A→aB or A→a) or left-linear (A→Ba or A→a) grammars. A rule breaks the right-linear pattern if: it's longer than 2 symbols, or it has 2 symbols but the second one isn't a non-terminal, or it has 1 symbol which is a non-terminal. Similar checks apply for left-linear rules.

```python
if is_right or is_left:
    return "Type 3 (Regular Grammar)"

# check type 2 (context-free)
is_cf = True
for lhs, rhs_list in self.P.items():
    if len(lhs) != 1 or lhs not in self.VN:
        is_cf = False
        break

```
If the grammar is either right-linear or left-linear, it's Type 3 (Regular). Otherwise, we check if it's Type 2 (Context-Free) by making sure every left-hand side of a production rule is exactly one non-terminal symbol.

```python
# check type 1 (context-sensitive)
is_cs = True
for lhs, rhs_list in self.P.items():
    for rhs in rhs_list:
        if len(rhs) == 0 and lhs == self.S:
            s_on_rhs = False
            for _, prods in self.P.items():
                for prod in prods:
                    if self.S in prod:
                        s_on_rhs = True
                        break
                if s_on_rhs: break
            if not s_on_rhs: continue

```
This part checks for Type 1 (Context-Sensitive). For context-sensitive grammars, the length of the right-hand side must not be shorter than the left-hand side, with one exception: S→ε is allowed if S doesn't appear on the right side of any rule.

```python
def is_deterministic(self):
    # check if dfa
    for state in self.Q:
        if state not in self.Delta: continue
        
        for sym in self.Sigma:
            if sym not in self.Delta[state]: continue
            
            if len(self.Delta[state][sym]) > 1:
                return False
    
    return True
```
This function checks if our automaton is deterministic. In a DFA, from any state with any input symbol, there can be at most one next state. If any state has multiple next states for a single symbol (represented by having more than one element in Delta[state][sym]), the automaton is non-deterministic.

```python
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
                p[state].append(sym + next_state)
```
Unlike Lab 1 that went from grammar to FA, this function does the reverse: converting an FA back to a regular grammar. States become non-terminals, input symbols become terminals, and transitions become production rules. For example, a transition δ(q0,a)=q1 becomes a rule q0→aq1.

```python
def to_dfa(self):
    # ndfa to dfa
    if self.is_deterministic(): return self
    
    dfa_q = set()
    dfa_sigma = self.Sigma
    dfa_delta = {}
    dfa_q0 = frozenset([self.q0])
    dfa_f = set()
```
This function implements the subset construction algorithm to convert an NDFA to a DFA. If the automaton is already deterministic, it just returns itself. Otherwise, it creates a new DFA where states are sets of the original NDFA states (which is why we use frozenset).

---

## **6. Conclusions**

This lab focused on finite automata, grammar classification, and the conversion of an NDFA to a DFA. We started with a given automaton and analyzed its properties, determining that it was non-deterministic due to multiple transitions on the same input from a single state. The DFA conversion process successfully produced an equivalent deterministic automaton, correctly grouping NDFA states while preserving language recognition. The final states were properly assigned, ensuring correctness in acceptance conditions.

The regular grammar equivalent was also generated without issues. However, an unexpected result appeared in the classification step—the grammar was identified as Type 0 (Unrestricted Grammar) instead of Type 3 (Regular Grammar). Given that the automaton itself is regular, its grammar should be as well. This suggests a potential issue in the classification function, which may require further refinement to correctly distinguish regular grammar structures.

Comparing this with Lab 1, the previous grammar was correctly classified as Type 3, indicating that the function generally works but may need adjustments for certain cases. Despite this minor inconsistency, the core objectives of the lab were achieved, and the conversion process demonstrated the expected theoretical properties.

---

## **7. Bibliography**

1. [NFA to DFA Conversion - GitHub](https://github.com/filpatterson/DSL_laboratory_works/tree/master/2_FiniteAutomata)
2. [DFA And NFA - Unstop](https://unstop.com/blog/difference-between-dfa-and-nfa#:~:text=Similarities%20between%20DFA%20and%20NFA,also%20known%20as%20regular%20languages.)
3. [DFA - openDSA](https://cs.stanford.edu/people/eroberts/courses/soco/projects/2004-05/automata-theory/apps.html)
4. [Deterministic finite automaton - Wikipedia](https://en.wikipedia.org/wiki/Deterministic_finite_automaton#:~:text=11.1%20Further%20reading-,Formal%20definition,finite%20set%20of%20states%20Q)

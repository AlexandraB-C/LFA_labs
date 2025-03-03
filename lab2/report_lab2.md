# Report Laboratory Work 2

## MINISTERUL EDUCAȚIEI, CULTURII ȘI CERCETĂRII
### AL REPUBLICII MOLDOVA
#### Universitatea Tehnică a Moldovei  
**Facultatea Calculatoare, Informatică şi Microelectronică**  
**Departamentul Inginerie Software și Automatică**  

### **ALEXANDRA BUJOR-COBILI, FAF-232**  
#### **Report - Laboratory work n.2**  
#### **Formal Languages & Finite Automata**  

**Checked by:**  
*Cretu Dumitru, university prof.*  
*FCIM, UTM*  

**Chișinău – 2025**  

---

## **1. Theory**

### **Deterministic Finite Automata (DFA)**
**Definition:** A DFA is a finite-state machine that accepts or rejects a given string of symbols by running through a uniquely determined state sequence.  

**Formal Definition:**   
A DFA is a 5-tuple (Q, Σ, δ, q0, F), where:  
    * Q is a finite set of states.
    * Σ is a finite set of input symbols (the alphabet).
    * δ: Q × Σ → Q is the transition function (single-valued).
    * q0 ∈ Q is the initial state.
    * F ⊆ Q is the set of accepting (final) states.  

**Key Characteristic:** For each state and input symbol, there is *exactly one* transition.  

**Applications:** Used in lexical analysis, pattern matching, and other areas requiring deterministic behavior.

### **Non-deterministic Finite Automata (NDFA)**
**Definition:** An NDFA allows for multiple possible transitions from a given state on the same input symbol, or ε-transitions.

**Formal Definition:**   
An NDFA is a 5-tuple (Q, Σ, δ, q0, F), where:  
    * δ: Q × (Σ ∪ {ε}) → 2^Q (transition function maps to a set of states).

**Key Characteristic:** Allows multiple transitions or ε-transitions.

**Acceptance:** An NDFA accepts a string if *at least one* of the possible state sequences leads to an accepting state.

**Equivalence:** NDFAs are equivalent in power to DFAs, meaning any language accepted by an NDFA can also be accepted by a DFA.

### **NDFA to DFA Conversion (Subset Construction)**
**Subset Construction (Powerset Construction):**
    * The primary method for converting an NDFA to a DFA.
    * Creates DFA states that represent sets of NDFA states.

**Detailed Process:**  
    * Start with the initial DFA state as the ε-closure of the NDFA's initial state.
    * For each DFA state and input symbol, calculate the set of NDFA states reachable. This becomes a new DFA state.
    * Repeat until no new DFA states are generated.
    * A DFA state is accepting if it contains at least one NDFA accepting state.
    * **Result:** The resulting DFA recognizes the same language as the original NDFA.
    * **Note:** The conversion can lead to an exponential increase in the number of states.
    * **Proof:** This conversion proves the equivalence of NFA and DFA, in that they both accept the Regular Languages.

### **Chomsky Hierarchy**
**Classification:** Classifies formal grammars and languages into four types:
    * Type-0 (Recursively Enumerable)
    * Type-1 (Context-Sensitive)
    * Type-2 (Context-Free)
    * Type-3 (Regular)

**Inclusion:** Type-3 ⊆ Type-2 ⊆ Type-1 ⊆ Type-0.

**Automata and Grammars:** Each grammar type corresponds to a specific type of automaton.

### **Grammar Types**  
**Type-0 (Recursively Enumerable):**
    * Unrestricted grammars.
    * Recognized by Turing machines.
    * Models general computation.

**Type-1 (Context-Sensitive):**
    * Production rules: αAβ → αγβ.
    * Recognized by linear bounded automata.
    * The length of the right side of a production rule is greater than or equal to the left side.

**Type-2 (Context-Free):**
    * Production rules: A → γ.
    * Recognized by pushdown automata.
    * Base of most programming language syntax.
    
**Type-3 (Regular):**
    * Production rules: A → aB or A → a.
    * Recognized by finite automata.
    * Used for simple pattern matching and lexical analysis.

---

## **2. Objectives**

1.  **Understand Automata:**
    * Gain a clear understanding of the definition, structure, and purpose of finite automata as models for various processes.
    * Comprehend the concept of states, transitions, and the distinction between starting and final states.

2.  **Chomsky Hierarchy Classification:**
    * Extend the existing grammar type/class within the project to include a function that accurately classifies grammars based on the Chomsky hierarchy.
    * Utilize the grammar variant from the previous lab as a foundation for this implementation.

3.  **Finite Automaton Operations (Variant-Specific):**
    **a. FA to Regular Grammar Conversion:** Implement a function or algorithm to convert the given finite automaton into its equivalent regular grammar representation.
    **b. Determinism Analysis:** Determine and report whether the specified finite automaton is deterministic (DFA) or non-deterministic (NDFA).
    **c. NDFA to DFA Conversion (if applicable):** If the automaton is non-deterministic, implement a function or algorithm to convert it into an equivalent deterministic finite automaton (DFA).
    **d. Graphical Representation (Optional Bonus):**
            * Develop a method to generate a visual representation (diagram) of the finite automaton.
            * This can be achieved using external libraries, tools, or APIs.
            * The program should automatically extract the automaton's data and interface with the chosen visualization method.
            * Alternatively, provide a detailed manual representation and explanation in the report.

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
            
            # check right-linear (A→aB or A→a)
            if len(rhs) > 2 or (len(rhs) == 2 and rhs[1] not in self.VN) or (len(rhs) == 1 and rhs[0] in self.VN):
                is_right = False
            
            # check left-linear (A→Ba or A→a)
            if len(rhs) > 2 or (len(rhs) == 2 and rhs[0] not in self.VN) or (len(rhs) == 1 and rhs[0] in self.VN):
                is_left = False
```

The grammar classification function checks what type a grammar is. It looks at all the rules to see if they follow specific patterns. For a regular grammar (Type 3), all rules must be either right-linear (like A→aB or A→a) or left-linear (like A→Ba or A→a). If rules don't follow these patterns, the function checks for other grammar types like context-free (Type 2) or context-sensitive (Type 1). If none of these types match, the grammar is considered unrestricted (Type 0).

```python
def classify_grammar(self):

```

The

```python
def classify_grammar(self):

```

The
```python
def classify_grammar(self):

```

The

---

## **6. Conclusions**

In this lab, we expanded on the concepts from Lab 1 by focusing on grammar classification and automata conversions. The terminal output clearly demonstrates the success of our implementation.
Starting with a non-deterministic finite automaton (NDFA), we can see from the output that:

The initial NDFA has 4 states (q0, q1, q2, q3) and accepts input symbols 'a' and 'b'
The automaton is correctly identified as non-deterministic with the output "deterministic? False" because q0 has two transitions for input 'a' (to both q1 and q2)
Our conversion to a regular grammar worked correctly, creating production rules like "q0 → aq1" and "q3 → ε" that preserve the automaton's behavior
Interestingly, while the grammar was created from an automaton that should be regular (Type 3), the classification function determined it was "Type 0 (Unrestricted Grammar)" - this could indicate a potential issue in our classification algorithm that needs further investigation
The DFA conversion process successfully created a deterministic equivalent with composite states like "{q0}", "{q1,q2}", "{q1,q3}", representing multiple possible states from the original NDFA
The final states in the DFA ({"{q1,q3}", "{q3}"}) correctly include any composite states containing the original final state q3

We also verified that our grammar from Lab 1 was properly classified as "Type 3 (Regular Grammar)", which confirms it works correctly for that case.
The visualization of both automata (which would appear after the text output) helps us understand the transformation process. The NDFA shows multiple transitions from q0 with the same symbol, while the DFA shows a cleaner structure with exactly one transition per symbol from each state.

![Image1](./lab2/img/lab2.png)
![Image2](./lab2/img/nfa_diag.png)
![Image3](./lab2/img/dfa_diag.png)

---

## **7. Bibliography**

1. [NFA to DFA Conversion - GitHub](https://github.com/filpatterson/DSL_laboratory_works/tree/master/2_FiniteAutomata)
2. [DFA And NFA - Unstop](https://unstop.com/blog/difference-between-dfa-and-nfa#:~:text=Similarities%20between%20DFA%20and%20NFA,also%20known%20as%20regular%20languages.)
3. [DFA - openDSA](https://cs.stanford.edu/people/eroberts/courses/soco/projects/2004-05/automata-theory/apps.html)
4. [Deterministic finite automaton - Wikipedia](https://en.wikipedia.org/wiki/Deterministic_finite_automaton#:~:text=11.1%20Further%20reading-,Formal%20definition,finite%20set%20of%20states%20Q)

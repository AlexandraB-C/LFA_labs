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
* **Definition:** A DFA is a finite-state machine that accepts or rejects a given string of symbols by running through a uniquely determined state sequence.
* **Formal Definition:** A DFA is a 5-tuple (Q, Σ, δ, q0, F), where:
    * Q is a finite set of states.
    * Σ is a finite set of input symbols (the alphabet).
    * δ: Q × Σ → Q is the transition function (single-valued).
    * q0 ∈ Q is the initial state.
    * F ⊆ Q is the set of accepting (final) states.
* **Key Characteristic:** For each state and input symbol, there is *exactly one* transition.
* **Applications:** Used in lexical analysis, pattern matching, and other areas requiring deterministic behavior.

### **Non-deterministic Finite Automata (NDFA)**
* **Definition:** An NDFA allows for multiple possible transitions from a given state on the same input symbol, or ε-transitions.
* **Formal Definition:** An NDFA is a 5-tuple (Q, Σ, δ, q0, F), where:
    * δ: Q × (Σ ∪ {ε}) → 2^Q (transition function maps to a set of states).
* **Key Characteristic:** Allows multiple transitions or ε-transitions.
* **Acceptance:** An NDFA accepts a string if *at least one* of the possible state sequences leads to an accepting state.
* **Equivalence:** NDFAs are equivalent in power to DFAs, meaning any language accepted by an NDFA can also be accepted by a DFA.

#### **NDFA to DFA Conversion (Subset Construction)**
* **Subset Construction (Powerset Construction):**
    * The primary method for converting an NDFA to a DFA.
    * Creates DFA states that represent sets of NDFA states.
* **Detailed Process:**
    * Start with the initial DFA state as the ε-closure of the NDFA's initial state.
    * For each DFA state and input symbol, calculate the set of NDFA states reachable. This becomes a new DFA state.
    * Repeat until no new DFA states are generated.
    * A DFA state is accepting if it contains at least one NDFA accepting state.
    * **Result:** The resulting DFA recognizes the same language as the original NDFA.
    * **Note:** The conversion can lead to an exponential increase in the number of states.
    * **Proof:** This conversion proves the equivalence of NFA and DFA, in that they both accept the Regular Languages.

##### **Chomsky Hierarchy**
* **Classification:** Classifies formal grammars and languages into four types:
    * Type-0 (Recursively Enumerable)
    * Type-1 (Context-Sensitive)
    * Type-2 (Context-Free)
    * Type-3 (Regular)
* **Inclusion:** Type-3 ⊆ Type-2 ⊆ Type-1 ⊆ Type-0.
* **Automata and Grammars:** Each grammar type corresponds to a specific type of automaton.

### Grammar Types

* **Type-0 (Recursively Enumerable):**
    * Unrestricted grammars.
    * Recognized by Turing machines.
    * Models general computation.
* **Type-1 (Context-Sensitive):**
    * Production rules: αAβ → αγβ.
    * Recognized by linear bounded automata.
    * The length of the right side of a production rule is greater than or equal to the left side.
* **Type-2 (Context-Free):**
    * Production rules: A → γ.
    * Recognized by pushdown automata.
    * Base of most programming language syntax.
* **Type-3 (Regular):**
    * Production rules: A → aB or A → a.
    * Recognized by finite automata.
    * Used for simple pattern matching and lexical analysis.

### Significance

* Provides a framework for understanding the expressive power of formal languages.
* Defines the computational power of machines that recognize them.
* Foundational concept in computer science and formal language theory.

---

## **2. Objectives**

1.  **Understand Automata:**
    * Gain a clear understanding of the definition, structure, and purpose of finite automata as models for various processes.
    * Comprehend the concept of states, transitions, and the distinction between starting and final states.

2.  **Chomsky Hierarchy Classification:**
    * Extend the existing grammar type/class within the project to include a function that accurately classifies grammars based on the Chomsky hierarchy.
    * Utilize the grammar variant from the previous lab as a foundation for this implementation.

3.  **Finite Automaton Operations (Variant-Specific):**
    * Based on the provided finite automaton definition (determined by the student's register ID), perform the following tasks:
        * **a. FA to Regular Grammar Conversion:** Implement a function or algorithm to convert the given finite automaton into its equivalent regular grammar representation.
        * **b. Determinism Analysis:** Determine and report whether the specified finite automaton is deterministic (DFA) or non-deterministic (NDFA).
        * **c. NDFA to DFA Conversion (if applicable):** If the automaton is non-deterministic, implement a function or algorithm to convert it into an equivalent deterministic finite automaton (DFA).
        * **d. Graphical Representation (Optional Bonus):**
            * Develop a method to generate a visual representation (diagram) of the finite automaton.
            * This can be achieved using external libraries, tools, or APIs.
            * The program should automatically extract the automaton's data and interface with the chosen visualization method.
            * Alternatively, provide a detailed manual representation and explanation in the report.
    * Provide a manual, detailed report, that explains all conversion and changes that were performed.
    * Provide a program that will convert any given finite automata to a regular grammar, as a bonus point.

---

## **5. Implementation**

### **Variant 4 (past lab):**
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
### **Variant 4:**
Q = {q0,q1,q2,q3},
∑ = {a,b},
F = {q3},
δ(q0,a) = q1,
δ(q0,a) = q2,
δ(q1,b) = q1,
δ(q1,a) = q2,
δ(q2,a) = q1,
δ(q2,b) = q3.


**Code explanation**
```python
def __init__(self, vn, vt, p, s):
        self.vn = vn
        self.vt = vt
        self.p = p
        self.s = s
```

This is storing the basic parts needed for a grammar, following the formal definition of a Context-Free Grammar (CFG) which requires these four components. From the main function example, we can see it takes things like vn = {'S', 'L', 'D'} (non-terminals - variables that can be replaced), vt = {'a', 'b', 'c', 'd', 'e', 'f', 'j'} (terminals - symbols that appear in final strings), production rules (P), and a start symbol 'S'. These components follow the standard CFG notation G = (V, Σ, P, S) where V is our vn, Σ is our vt, P is our production rules, and S is our start symbol.  
Basically storing the building blocks we'll use later.



```python
def gen_str(self, max_iter=50):
        curr = self.s
        i = 0
       
        while i < max_iter:
            # check no more nonterminals
            if all(sym not in self.vn for sym in curr):
                return curr
```
The string generator (gen_str):
This implements the leftmost derivation process in formal grammars. For example, it might start with 'S' and use the rule ('S', 'aS') to get 'aS', then maybe ('S', 'e') to end up with 'ae'. Each step represents a derivation in the grammar, written as S ⇒ aS ⇒ ae in formal notation. The max_iter parameter prevents infinite recursion in case of left-recursive grammars, which is a common concern in grammar implementation.


```python
def gen_mult_strs(self, cnt=5):
        strs = set()
        tries = 0
        max_tries = cnt * 20
       
        while len(strs) < cnt and tries < max_tries:
            if res := self.gen_str():
                if all(c in self.vt for c in res):
                       strs.add(res)
```
The multiple string generator (gen_mult_strs):
This generates multiple strings from the grammar's language L(G). It creates a sample of the language, demonstrating that our grammar can generate different strings that belong to the same language. From the main function, we see it makes 5 different strings like 'e', 'ae', 'be', etc. This relates to the concept of language generation in formal language theory, where L(G) is the set of all possible strings that can be derived from the grammar.


```python
def to_fa(self):
        # convert
        states = self.vn | {'F'}
        alpha = self.vt
        trans = {}
...

```
The grammar to FA converter (to_fa):
This implements a transformation from a right-linear grammar to a finite automaton, which is a fundamental concept in formal language theory. The rule ('S', 'aS') becomes a transition δ(S,a) = S in automaton notation. This transformation demonstrates the equivalence between right-linear grammars and regular languages, showing how different representations can define the same language.


```python
def check_str(self, inp):
        curr_states = {self.init}
       
        for c in inp:
            if c not in self.alpha:
                return False
```
The string checker (check_str):
This implements the deterministic finite automaton (DFA) acceptance process. For each input symbol, it follows the transition function δ to move between states. The acceptance condition checks if the final state is reached, implementing the formal definition of language acceptance in automata theory. In formal notation, it checks if δ*(q₀,w) ∈ F where q₀ is the initial state and F is the set of final states.

**Key functions:**
- **Grammar Initialization:** Defines variables, terminals, production rules, and start symbol.
- **String Generation:** Implements leftmost derivation.
- **Multiple String Generation:** Demonstrates language generation.
- **Grammar to FA Conversion:** Converts a right-linear grammar into a finite automaton.
- **String Checking in FA:** Implements DFA acceptance process.

```python
g = Grammar(vn, vt, p, s)
strings = g.gen_mult_strs(5)
fa = g.to_fa()
```

---

## **6. Conclusions**

In this lab, we tested how formal languages and finite automata work together. First, we defined a grammar using a set of rules that generate valid strings. Then, we implemented a program to generate multiple valid strings using random rule applications. After that, we converted the grammar into a finite automaton (FA), treating non-terminals as states and terminals as transitions. We tested the FA by checking if different input strings were accepted or rejected. 

the output see in pdf

From the results, we can see that:
- Valid strings were generated based on the rules.
- The FA successfully identified correct and incorrect strings, proving the correctness of our conversion.
- The program worked without errors, confirming that the logic was implemented properly.

Overall, this lab helped us understand how formal languages define patterns and how finite automata validate them efficiently.

---

## **7. Bibliography**

1. [NFA to DFA Conversion - GitHub](https://github.com/filpatterson/DSL_laboratory_works/tree/master/2_FiniteAutomata)
2. [DFA And NFA - Unstop](https://unstop.com/blog/difference-between-dfa-and-nfa#:~:text=Similarities%20between%20DFA%20and%20NFA,also%20known%20as%20regular%20languages.)
3. [DFA - openDSA](https://cs.stanford.edu/people/eroberts/courses/soco/projects/2004-05/automata-theory/apps.html)
4. [Deterministic finite automaton - Wikipedia](https://en.wikipedia.org/wiki/Deterministic_finite_automaton#:~:text=11.1%20Further%20reading-,Formal%20definition,finite%20set%20of%20states%20Q)

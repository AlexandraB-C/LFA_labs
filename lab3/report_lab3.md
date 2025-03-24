# Report Laboratory Work 3

## MINISTERUL EDUCAȚIEI, CULTURII ȘI CERCETĂRII
### AL REPUBLICII MOLDOVA
#### Universitatea Tehnică a Moldovei  
**Facultatea Calculatoare, Informatică și Microelectronică**  
**Departamentul Inginerie Software și Automatică**  

### **ALEXANDRA BUJOR-COBILI, FAF-232**  
#### **Report - Laboratory work n.3**  
#### **Lexer & Scanner Implementation**  

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

---

## **2. Objectives**

1. Understand what lexical analysis [1] is.
2. Get familiar with the inner workings of a lexer/scanner/tokenizer.
3. Implement a sample lexer and show how it works. 

---

## **5. Implementation**

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


---

## **6. Conclusions**

This lab focused on finite automata, grammar classification, and the conversion of an NDFA to a DFA. We started with a given automaton and analyzed its properties, determining that it was non-deterministic due to multiple transitions on the same input from a single state. The DFA conversion process successfully produced an equivalent deterministic automaton, correctly grouping NDFA states while preserving language recognition. The final states were properly assigned, ensuring correctness in acceptance conditions.

The regular grammar equivalent was also generated without issues. However, in a previous atempt, an unexpected result appeared in the classification step—the grammar was identified as Type 0 instead of Type 2. Given that the automaton itself is context-free, its grammar should be as well. This suggests a potential issue in the classification function, which may require further refinement to correctly distinguish regular grammar structures, that is what i would say if i left the code as it was, duh.

Comparing this with Lab 1, the previous grammar was correctly classified as Type 3, indicating that the function generally works and does not need adjustments for certain cases. Despite this minor inconsistency, the core objectives of the lab were achieved, and the conversion process demonstrated the expected theoretical properties.

---

## **7. Bibliography**

1. [NFA to DFA Conversion - GitHub](https://github.com/filpatterson/DSL_laboratory_works/tree/master/2_FiniteAutomata)
2. [DFA And NFA - Unstop](https://unstop.com/blog/difference-between-dfa-and-nfa#:~:text=Similarities%20between%20DFA%20and%20NFA,also%20known%20as%20regular%20languages.)
3. [DFA - openDSA](https://cs.stanford.edu/people/eroberts/courses/soco/projects/2004-05/automata-theory/apps.html)
4. [Deterministic finite automaton - Wikipedia](https://en.wikipedia.org/wiki/Deterministic_finite_automaton#:~:text=11.1%20Further%20reading-,Formal%20definition,finite%20set%20of%20states%20Q)

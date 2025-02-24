# Report Laboratory Work 1

## MINISTERUL EDUCAȚIEI, CULTURII ȘI CERCETĂRII
### AL REPUBLICII MOLDOVA
#### Universitatea Tehnică a Moldovei  
**Facultatea Calculatoare, Informatică şi Microelectronică**  
**Departamentul Inginerie Software și Automatică**  

### **ALEXANDRA BUJOR-COBILI, FAF-232**  
#### **Report - Laboratory work n.1**  
#### **Formal Languages & Finite Automata**  

**Checked by:**  
*Cretu Dumitru, university prof.*  
*FCIM, UTM*  

**Chișinău – 2025**  

---

## **1. Theory**

### **Key Components of a Formal Language**
A formal language can be considered as the medium used to convey information from a sender to a receiver. It consists of:
- **Alphabet:** Set of valid characters.
- **Vocabulary:** Set of valid words.
- **Grammar:** Set of rules/constraints over the language.

Different configurations of these components define various formal, natural, programming, and markup languages.

### **Finite Automata and Their Role**
A finite automaton (FA) is a computational model used to recognize patterns and validate strings against a given formal language. It consists of:
- **Finite set of states (Q):** Possible conditions the automaton can be in.
- **Alphabet (Σ):** Set of input symbols.
- **Transition function (δ):** Defines state changes based on input.
- **Start state (q₀):** The initial state.
- **Final states (F):** Accepting states.

#### **Conversion from Grammar to Finite Automaton**
A right-linear grammar (where non-terminals appear at the end of production rules) can be converted into a finite automaton by treating non-terminals as states and terminals as transitions.

##### **Example Grammar:**
```
Start symbol = S
Non-terminals = {S}
Terminals = {a, b}
Production rules: S → aSb, S → ba

Example derivations:
S → aSb → abab
S → aSb → aaSbb → aababb

Language (L) = {abab, aababb, ...}
```

---

## **2. Historical Background**

The concept of finite automata dates back to the early 20th century. Some key milestones include:
- **1936:** Alan Turing introduced the Turing machine.
- **1940s-1950s:** Warren McCulloch and Walter Pitts proposed neural networks based on binary logic.
- **1956:** Noam Chomsky introduced the Chomsky hierarchy.
- **1956:** Michael Rabin and Dana Scott formally defined DFA and NFA, proving their equivalence. They received the Turing Award in 1976.
- **John Myhill & Raymond Moore:** Developed state minimization techniques.

---

## **3. Limitations of Finite Automata**

While FA are powerful in many areas, they have some limitations:
- **Lack of Memory:** FA cannot recognize non-regular languages (e.g., balancing parentheses).
- **Inability to Process Context-Free Languages:** FA cannot handle nested structures (e.g., arithmetic expressions).
- **State Explosion Problem:** DFA conversion from an NFA can lead to an exponential increase in the number of states.

---

## **4. Applications of Automata Theory**

Automata are widely used in:
- **Lexical analysis:** Compilers use FA to identify keywords and tokens.
- **Pattern matching:** FA are used in regex engines and text search algorithms.
- **Network security:** Packet validation in firewalls.
- **Artificial Intelligence & NLP:** Speech and text processing.

---

## **5. Objectives**

- Understand what constitutes a formal language.
- Set up the foundation for the semester-long project.
- Implement a grammar and finite automaton in a programming language.

**Tasks:**
1. Create a GitHub repository to store and update the project.
2. Choose a programming language suitable for implementation.
3. Implement the following:
   - Define a grammar.
   - Generate 5 valid strings from the grammar.
   - Convert the grammar into a finite automaton.
   - Implement a method to validate strings using the FA.

---

## **6. Implementation**

### **Variant 4:**
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

## **7. Conclusions**

In this lab, we explored the relationship between formal languages and finite automata:
- **Defined a grammar** with production rules.
- **Generated valid strings** using the grammar.
- **Converted the grammar into a finite automaton.**
- **Tested FA to validate input strings.**

**Key takeaways:**
- The FA successfully identified valid and invalid strings.
- The conversion process from grammar to FA was successful.
- The implementation proved correct without errors.

---

## **8. Bibliography**

1. [Regular Grammars - GitHub](https://github.com/filpatterson/DSL_laboratory_works/blob/master/1_RegularGrammars/task.md)
2. [Theory of Computation - GeeksforGeeks](https://www.geeksforgeeks.org/theory-of-computation-automata-tutorials/)
3. [Applications of Automata - Stanford](https://cs.stanford.edu/people/eroberts/courses/soco/projects/2004-05/automata-theory/apps.html)
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

## **2. Limitations of Finite Automata**

Finite Automata (FA) are powerful computational models, but they have some limitations that make them unsuitable for certain types of problems:

- **Lack of Memory:** FA do not have memory or the ability to count, meaning they cannot recognize non-regular languages. For example, they cannot determine whether a string has balanced parentheses (e.g., `((()))` vs. `(()))`). Since FA only process input sequentially without storing previous states, they fail in tasks requiring long-term dependencies.

- **Inability to Process Context-Free Languages:** FA are incapable of handling nested structures, such as arithmetic expressions with multiple levels of parentheses (e.g., `(a + (b * c))`). These structures require memory to track which parts belong together, something FA lacks. Context-free languages, which require pushdown automata (PDA) to be processed correctly, cannot be handled by FA.

- **State Explosion Problem:** When converting a Nondeterministic Finite Automaton (NFA) into a Deterministic Finite Automaton (DFA), the number of states can grow exponentially. This results in an impractical number of states for complex languages, making FA inefficient in certain scenarios. Large state spaces also increase computation time and storage requirements.

---

## **3. Applications of Automata Theory**

Despite these limitations, Automata Theory is widely used in various fields of computer science and technology:

- **Lexical Analysis:** Compilers use FA to analyze and break down source code into tokens, such as keywords, operators, and identifiers. This is the first step in compiling a programming language and helps ensure that code follows the correct syntax.

- **Pattern Matching:** FA play a crucial role in text searching algorithms, particularly in regular expression (regex) engines. Applications like search engines, text editors, and data validation tools rely on FA to identify specific patterns in large text files quickly and efficiently.

- **Network Security:** FA are used in firewalls and intrusion detection systems for packet validation. They help determine whether network packets conform to expected security rules, blocking malicious traffic and improving cybersecurity.

- **Artificial Intelligence & NLP:** In natural language processing (NLP), FA are used in tasks like speech recognition, text processing, and chatbots. They help in parsing sentences, identifying word structures, and processing simple language commands in AI applications.

---

## **4. Objectives**

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

## **5. Implementation**

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

1. [Regular Grammars - GitHub](https://github.com/filpatterson/DSL_laboratory_works/blob/master/1_RegularGrammars/task.md)
2. [Theory of Computation - GeeksforGeeks](https://www.geeksforgeeks.org/theory-of-computation-automata-tutorials/)
3. [Applications of Automata - Stanford](https://cs.stanford.edu/people/eroberts/courses/soco/projects/2004-05/automata-theory/apps.html)

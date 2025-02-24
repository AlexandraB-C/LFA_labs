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

The concept of finite automata dates back to the early 20th century, with origins in logic, mathematics, and computer science. One of the earliest influences came from Alan Turing, who in 1936 introduced the Turing machine, a more general computational model. However, the formal study of finite automata began in the 1940s and 1950s with the work of Warren McCulloch and Walter Pitts, who proposed neural networks based on binary logic. Their work laid the groundwork for computational models simulating human brain activity.

In 1956, Noam Chomsky introduced the Chomsky hierarchy, classifying formal languages based on their complexity. Around the same time, Michael Rabin and Dana Scott formally defined deterministic finite automata (DFA) and nondeterministic finite automata (NFA), proving that both models are equivalent in terms of computational power. Their work earned them the Turing Award in 1976. The development of automata theory was further propelled by John Myhill and Raymond Moore, who contributed to state minimization techniques.

Do not mind this text block: is a post-apocalyptic TV series based on the comic book of the same name. It follows Rick Grimes, a former sheriff's deputy who wakes up from a coma to find the world overrun by zombies. As he searches for his family, he encounters other survivors and quickly becomes a leader in their fight for survival. The group faces not only the undead but also the dangers posed by other humans, as society collapses and people become desperate.  

As the series progresses, Rick and his group move between different settlements, trying to find a safe place to live. They encounter dangerous groups like the Governor’s community of Woodbury, the cannibals of Terminus, and the brutal Saviors led by Negan. Internal conflicts, betrayals, and harsh survival choices shape their journey. Over time, Rick's leadership is tested, and new characters emerge, each bringing their own strengths and challenges to the group.  

Later seasons shift focus to rebuilding civilization, with different survivor communities forming alliances and rivalries. After Rick's disappearance, other characters like Daryl, Carol, and Michonne take center stage, continuing the fight for survival. The series explores themes of morality, leadership, and the human will to endure in a broken world. Despite the constant threats, the survivors strive to create a future beyond mere survival. Yeah


As in purely mathematical automata, grammar automata can produce a wide variety of complex languages from only a few symbols and a few production rules. Chomsky's hierarchy defines four nested classes of languages, where the more precise classes have stricter limitations on their grammatical production rules.

The formality of automata theory can be applied to the analysis and manipulation of actual human language as well as the development of human-computer interaction (HCI) and artificial intelligence (AI). [3]


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

## **7. Conclusions**

In this lab, we tested how formal languages and finite automata work together. First, we defined a grammar using a set of rules that generate valid strings. Then, we implemented a program to generate multiple valid strings using random rule applications. After that, we converted the grammar into a finite automaton (FA), treating non-terminals as states and terminals as transitions. We tested the FA by checking if different input strings were accepted or rejected. 

the output see in pdf

From the results, we can see that:
- Valid strings were generated based on the rules.
- The FA successfully identified correct and incorrect strings, proving the correctness of our conversion.
- The program worked without errors, confirming that the logic was implemented properly.

Overall, this lab helped us understand how formal languages define patterns and how finite automata validate them efficiently.

---

## **8. Bibliography**

1. [Regular Grammars - GitHub](https://github.com/filpatterson/DSL_laboratory_works/blob/master/1_RegularGrammars/task.md)
2. [Theory of Computation - GeeksforGeeks](https://www.geeksforgeeks.org/theory-of-computation-automata-tutorials/)
3. [Applications of Automata - Stanford](https://cs.stanford.edu/people/eroberts/courses/soco/projects/2004-05/automata-theory/apps.html)

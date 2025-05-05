# Report Laboratory Work 5

## MINISTERUL EDUCAȚIEI, CULTURII ȘI CERCETĂRII
### AL REPUBLICII MOLDOVA
#### Universitatea Tehnică a Moldovei  
**Facultatea Calculatoare, Informatică și Microelectronică**  
**Departamentul Inginerie Software și Automatică**  

### **ALEXANDRA BUJOR-COBILI, FAF-232**  
#### **Report - Laboratory work n.5**  
#### **Chomsky Normal Form**  

**Checked by:**  
*Cretu Dumitru, university assistant*  
*FCIM, UTM*  

**Chișinău – 2025**  

---

## **1. Theory**
#### **1.1. Chomsky Normal Form**
Chomsky Normal Form (CNF) is a special way to write context-free grammars. In Chomsky Normal Form, each production rule must have a specific form. The rules are easier to work with in CNF and are very helpful in parsing.

A grammar is in CNF if all of its rules follow one of these patterns:
1. A → BC (A, B, and C are non-terminal symbols)
2. A → a (a is a terminal symbol)
3. S → ε (S is the start symbol and ε means an empty string)

#### **1.2. Key Consepts**
Each CFG can be changed into an equivalent CNF. The new grammar will generate the same language as the original one. CNF is also helpful because it keeps grammar small and simple.

Steps to follow: 
1. Eliminate ε-Productions  

An ε-production is a rule like A → ε. These must be removed, except for the new start symbol. We find which variables can go to ε (nullable), then change the rules to cover all possible combinations without ε. Finally, we remove the ε-rules.

2. Remove Unit Productions

A unit production is a rule like A → B, where both are variables. To remove them, we replace A → B with all rules from B. This way, A directly gets the rules that B had.

3. Replace Terminals in Mixed Rules

Sometimes we have rules like A → aB or A → Ba. These are not allowed in CNF. We replace the terminals with new variables. For example, if we have A → aB, we create X → a and replace it with A → X_B.

4. Break Long Rules into Binary Rules

CNF only allows two symbols on the right-hand side. If a rule has more than two, like A → BCD, we break it into steps. We create new variables: A → B_X1, X1 → CD. This makes all rules binary.


#### **1.3. Example**
Consider the following grammar:  
```
S → ASB
A → aAS | a | ε
B → SbS | A | bb
```

We remove ε from A → aAS | a → aAS, aS, a  
Remove ε from B → A → B gets A’s rules  
Replace terminals: a, b → X, Y and use X and Y instead, also break long rules like ASB into smaller ones

After doing all steps, we get a grammar where each rule is in CNF. This makes the grammar ready for parsing and analysis.


---

## **2. Objectives**

1. Learn about Chomsky Normal Form (CNF) [1].
2. Get familiar with the approaches of normalizing a grammar.
3. Implement a method for normalizing an input grammar by the rules of CNF.
    1. The implementation needs to be encapsulated in a method with an appropriate signature (also ideally in an appropriate class/type).
    2. The implemented functionality needs executed and tested.
    3. Also, another **BONUS point** would be given if the student will make the aforementioned function to accept any grammar, not only the one from the student's variant.

#### **Variant 4:**
1. Eliminate ε productions
2. Eliminate any renaming
3. Eliminate inaccessible symbols
4. Eliminate non productive symbols
5. Convert to CNF form  
```
G = (Vn, Vt, P, S)
Vn = {S, A, B, C, D}
Vt = {a, b}

P = {
    S → aB
    S → bA
    S → A
    A → B
    A → AS
    A → bBAB
    A → b
    B → b
    B → bS
    B → aD
    B → ε
    D → AA
    C → Ba
}
```

---

## **3. Implementation**

#### **3.1. Epsilon elimination**
```python
def eliminate_epsilon_productions(grammar):
    nullable = set()
    for left, right_sides in grammar.p.items():
        if 'ε' in right_sides:
            nullable.add(left)
            right_sides.remove('ε')
```

This function begins by identifying all variables that can produce epsilon. It adds these variables to the nullable set and removes the ε symbol from their productions. Later, it generates new rules by removing nullable symbols in all possible combinations. This helps clean the grammar from empty strings.

#### **3.2. Unit productions**

```python
def eliminate_unit_productions(grammar):
    unit_pairs = set()
    for nt in grammar.vn:
        unit_pairs.add((nt, nt))
```
This function removes rules where one variable only produces another single variable. First, it creates a set of unit pairs. Then it looks for such relationships and adds the final productions to the correct variables. This process ensures that we no longer rely on indirect chains like A → B → C.

#### **3.3. Inaccessible symbols**

```python
def find_accessible_symbols(grammar):
    accessible = {grammar.s}
    changed = True
    while changed:
        changed = False
        for left in list(accessible):
            if left in grammar.p:
                for right in grammar.p[left]:
                    for symbol in right:
                        if symbol in grammar.vn and symbol not in accessible:
                            accessible.add(symbol)
                            changed = True
```
This function finds all variables that can be reached from the start symbol. It uses a loop to add every reachable symbol to the accessible set. Any variables not in this set are removed from the grammar. This step helps simplify the grammar by cutting out unused parts.

#### **3.4. Non-productive symbols**

```python
def find_productive_symbols(grammar):
    productive = set()
    for left, right_sides in grammar.p.items():
        for right in right_sides:
            if all(symbol in grammar.vt for symbol in right):
                productive.add(left)
```
The purpose of this function is to find all symbols that can lead to terminal strings. First, it checks for directly productive variables. Then it searches for indirectly productive ones. Variables that do not help generate real words are considered non-productive and are removed.

#### **3.5. Convert to CNF**

```python
def convert_to_cnf(grammar):
    terminal_replacements = {}
    new_productions = {left: set() for left in grammar.p}
```
This is the beginning of the conversion to CNF. It creates a dictionary to keep track of terminal replacements and prepares a new structure for the updated rules. The next steps in this function will replace terminals and split long rules into the proper format.

```python
for left, right_sides in grammar.p.items():
    for right in right_sides:
        if len(right) > 1:
            new_right = []
            for symbol in right:
                if symbol in grammar.vt:
                    if symbol not in terminal_replacements:
                        new_symbol = f"T_{symbol}"
                        terminal_replacements[symbol] = new_symbol
                        new_productions[new_symbol] = {symbol}
                    new_right.append(terminal_replacements[symbol])
                else:
                    new_right.append(symbol)
            new_productions[left].add(''.join(new_right))
```
This block replaces terminal symbols inside long rules with new variables. It ensures each terminal appears alone on the right-hand side when needed. This step is essential for meeting CNF format requirements.

```python
for left, right_sides in new_productions.items():
    for right in right_sides:
        if len(right) > 2:
            current_left = left
            for i in range(len(right) - 2):
                new_symbol = f"X_{left}_{i}"
                final_productions[current_left].add(right[i] + new_symbol)
                current_left = new_symbol
            final_productions[current_left].add(right[-2:])
        else:
            final_productions[left].add(right)
```
This final step ensures that each rule contains only two variables on the right-hand side. For longer rules, it creates intermediate variables that chain the symbols correctly. This restructuring completes the CNF transformation.

---

## **4. Conclusions**

In this laboratory work, we created and tested a Python program that converts a context-free grammar (CFG) into Chomsky Normal Form (CNF). The goal of the program was to take any grammar and make sure all the rules follow the CNF format. This means that each production rule must be either: a variable that goes to two variables (A → BC), a variable that goes to one terminal (A → a), or the start symbol going to an empty string (S → ε). 

How it works: it removes all epsilon (ε) rules, which are rules that produce an empty string. Then it removes unit rules, which are rules like A → B where both sides are variables. After that, the program removes any variables or rules that are not useful, such as symbols that cannot be reached or that never produce any terminal symbols. Then, it replaces terminals in longer rules with new variables, so that terminals do not appear together with other symbols. Finally, it changes any rules that have more than two symbols on the right side into smaller rules using new variables, so all rules become binary.

After running the program with a grammar from assigned variant, we can see from the result (lab5/image.png) that the program gives a correct CNF version. All the rules in the final output follow the CNF rules. Great success yupiii.

However, the program may not work perfectly for every grammar. For example, if the input grammar is very large or has many complex rules with ε-productions and unreachable symbols, the program will have a bad time. Also, the size of the grammar can grow a lot after the conversion. This is a normal problem in CNF transformations, but it can make the final grammar harder to use.

In general, this lab helped us understand how CNF works in practice. The program followed the main rules of CNF conversion and produced a correct result. With some improvements, it could work with more types of grammars and be used in more advanced parsing tasks.

---

## **5. Bibliography**

1. [Chomsky Normal Form (GitHub)](https://github.com/filpatterson/DSL_laboratory_works/blob/master/5_ChomskyNormalForm/task.md)
2. [Chomsky Normal Form Wiki (Wikipedia)](https://en.wikipedia.org/wiki/Chomsky_normal_form)
3. [Converting Context Free Grammar to Chomsky Normal Form (GeeksforGeeks)](https://www.geeksforgeeks.org/converting-context-free-grammar-chomsky-normal-form/)
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

### **L:**
**Definition:** L
### **Key Concepts:** 

### **C:**
### **Variant 4:**
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

## **2. Objectives**

1. Learn about Chomsky Normal Form (CNF) [1].
2. Get familiar with the approaches of normalizing a grammar.
3. Implement a method for normalizing an input grammar by the rules of CNF.
    1. The implementation needs to be encapsulated in a method with an appropriate signature (also ideally in an appropriate class/type).
    2. The implemented functionality needs executed and tested.
    3. Also, another **BONUS point** would be given if the student will make the aforementioned function to accept any grammar, not only the one from the student's variant.

---

## **3. Implementation**

### **Code explanation**  
#### **3.1. Token Types**
```python
from enum import Enum, auto

class TokenType(Enum):
    NUMBER = auto()
    IDENTIFIER = auto()
    OPERATOR = auto()
    FUNCTION = auto()
    LPAREN = auto()
    RPAREN = auto()
    ASSIGNMENT = auto()
    EOF = auto()
```

This code defines an enumeration that categorizes all possible token types our lexer can recognize:
- `NUMBER`: Represents numeric values (integers or floating-point)
- `IDENTIFIER`: Represents variable names or other identifiers
- `OPERATOR`: Represents mathematical operators (+, -, *, /, ^)
- `FUNCTION`: Represents built-in functions (sin, cos)
- `LPAREN` and `RPAREN`: Represent left and right parentheses
- `ASSIGNMENT`: Represents the assignment operator (=)
- `EOF`: Represents the end of the input  

Using `Enum` makes the code cleaner than just using strings. The `auto()` function gives each type a unique number automatically.

#### **3.2. Token Class**

```python
class Token:
    def __init__(self, type, value, position):
        self.type = type
        self.value = value
        self.position = position
    
    def __str__(self):
        return f"Token({self.type}, '{self.value}', pos={self.position})"
    
    def __repr__(self):
        return self.__str__()
```

This class is like a container for token information:
- `type`: What kind of token it is
- `value`: The actual text of the token
- `position`: Where the token starts in the input

The `__str__` and `__repr__` methods just make tokens print nicely when I debug, showing something like `Token(TokenType.NUMBER, '42', pos=0)`.


---

## **6. Conclusions**

This lab centered on the implementation of a lexical analyzer capable of recognizing tokens from arithmetic expressions, including numbers, identifiers, operators, parentheses, and trigonometric functions. The lexer successfully processed a variety of inputs, demonstrating its ability to correctly categorize tokens and track their positions within the input string. The handling of basic arithmetic expressions, function calls, and variable assignments was generally accurate, aligning with the core objectives of the lab.

However, during testing, several inconsistencies were observed. Notably, the input '3..14 + 2' resulted in the lexer incorrectly producing two separate number tokens, '3.0' and '0.14', instead of flagging an error or interpreting it as a single invalid token. Similarly, the input 'a + b' produced two operator tokens, which is clearly an error. These issues indicate potential bugs in the lexer's handling of edge cases and invalid input formats, suggesting a need for more robust error handling and input validation.

Despite these shortcomings, the lexer's ability to track token positions and handle a wide range of valid inputs is commendable. The implementation of implicit multiplication in the 'a = 2 ( b + c )' case, while unconventional, highlights the lexer's flexibility and potential for handling more complex language features. Comparing this lab with previous assignments, the unexpected tokenization of '3..14' and 'a + b' suggests that while the lexer performs well under standard conditions, it requires further refinement to ensure accuracy and robustness across all possible inputs. The core objectives of the lab were largely achieved, but the identified bugs necessitate further debugging and testing to create a reliable and production-ready lexical analyzer.

---

## **7. Bibliography**

1. [Chomsky Normal Form (GitHub)](https://github.com/filpatterson/DSL_laboratory_works/blob/master/5_ChomskyNormalForm/task.md)
2. [Chomsky Normal Form Wiki (Wikipedia)](https://en.wikipedia.org/wiki/Chomsky_normal_form)


3. [LLVM Tutorial - Implementing a Lexer](https://llvm.org/docs/tutorial/MyFirstLanguageFrontend/LangImpl01.html)
4. [Regular Expressions Tutorial (RegexOne)](https://regexone.com/)
5. [How to Write a Lexer in Python](https://tomassetti.me/parsing-in-python/)
6. [Finite Automata (GeeksforGeeks)](https://www.geeksforgeeks.org/finite-automata-fa/)
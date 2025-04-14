# Report Laboratory Work 4

## MINISTERUL EDUCAȚIEI, CULTURII ȘI CERCETĂRII
### AL REPUBLICII MOLDOVA
#### Universitatea Tehnică a Moldovei  
**Facultatea Calculatoare, Informatică și Microelectronică**  
**Departamentul Inginerie Software și Automatică**  

### **ALEXANDRA BUJOR-COBILI, FAF-232**  
#### **Report - Laboratory work n.4**
#### **Regular Expressions**  

**Checked by:**  
*Cretu Dumitru, university assistant*  
*FCIM, UTM*  

**Chișinău – 2025**  

---

## **1. Theory**

### **Regular Expression:**
**Definition:** A regular expression is a sequence of characters that defines a search pattern. It is like a rulebook that describes how a string should be formed. The most basic example is just a letter. For example, `a` matches the letter "a". But regular expressions become powerful when combined with special symbols:

- `(A|B)` means "A or B"
- `*` means repeat 0 or more times
- `+` means repeat at least once
- `?` means 0 or 1 time
- `{n}` means exactly n times
- `{n,m}` means at least n and at most m times

These elements can be used together to build complex patterns. For example, `(S|T)(U|V)W*Y+24` means: pick "S" or "T", then "U" or "V", then zero or more "W", then one or more "Y", and finally the digits "2" and "4".

### **Key Concepts:**  
1. **Parse** the regular expression:  
   Go through each character and find groups, quantifiers, and individual symbols. Groups are detected by looking for parentheses, and inside the group, the options are separated by "|". The program must also find the quantifier that comes after a group or character.

2. **Build Tokens**:  
   After parsing, each part of the expression is stored as a token. A token can be a single character or a group with options. Each token also remembers if it has a quantifier like `*`, `+`, `{3}`, etc.

3. **Generate the Result**:  
   For each token, the program decides how many times to repeat the value (based on the quantifier). For groups, it randomly picks one of the options. For characters, it just uses the value. These are combined step by step to form the final string.

4. **Trace Each Step**:  
   The program also shows each decision it made. This is helpful for learning. You can see which character was picked, how many times it was added, and how the string grows after each step.


### **Variant 4:**

(S|T)(U|V)W*Y+24  
L(M|N)O{3}P*Q(2|3)  
R*S(T|U|V)W(X|Y|Z){2}  

Each of these includes character sequences, groups with alternatives, and quantifiers. The program should be able to produce different results each time based on random choices but all results must be valid according to the original expression.

Let’s take: 
```
(S|T)(U|V)W*Y+24
```

This means:
- Start with "S" or "T"
- Then "U" or "V"
- Then 0 or more "W"
- Then 1 or more "Y"
- Then the digits "2" and "4"

A possible output could be:
```
SUWWYY24
```

Basicaly we choose "S" from group (S|T), then choose "U" from group (U|V). Repeat "W" two times. Repeat "Y" two times. At last add "2" and add "4".
Another valid output could be `TVY24`, where "W" is not repeated and "Y" appears once.

---

## **2. Objectives**

1. Write and cover what regular expressions are, what they are used for;

2. For the variant do the following:

    a. Write a code that will generate valid combinations of symbols conform given regular expressions (examples will be shown). Be careful that idea is to interpret the given regular expressions dinamycally, not to hardcode the way it will generate valid strings. You give a set of regexes as input and get valid word as an output

    b. In case you have an example, where symbol may be written undefined number of times, take a limit of 5 times (to evade generation of extremely long combinations);

    c. **Bonus point**: write a function that will show sequence of processing regular expression (like, what you do first, second and so on)


---

## **3. Implementation**

### **Code explanation**  
```python
    while i < len(regex):
        if regex[i] == '(':
            depth = 1
            j = i + 1
            while depth > 0 and j < len(regex):
                if regex[j] == '(':
                    depth += 1
                elif regex[j] == ')':
                    depth -= 1
                j += 1
```
The loop goes through every character in the regex. If it sees `(`, it knows a group is starting. It continues to search until it finds the closing `)` and then splits the group by `|` to find all the options.

```python
            if depth == 0:
                options = regex[i+1:j-1].split('|')
                if j < len(regex) and regex[j] in '{*+?':
                    if regex[j] == '{':
                        k = j + 1
                        while k < len(regex) and regex[k] != '}':
                            k += 1
                        if k < len(regex):
                            quant = regex[j:k+1]
                            tokens.append(('group', options, quant))
                            i = k + 1
                        else:
                            tokens.append(('group', options, ''))
                            i = j
                    else:
                        tokens.append(('group', options, regex[j]))
                        i = j + 1
                else:
                    tokens.append(('group', options, ''))
                    i = j - 1
```
After finding a complete group, this code extracts the options by splitting the content by the pipe character. It then checks if the group is followed by a quantifier like *, +, ?, or a curly brace expression. For curly braces, it finds the complete quantifier by searching for the closing brace. Finally, it stores the group information (type, options, and quantifier) as a token in the list and updates the position in the regex.

```python
def apply_quant(text, quant, max=5):
    if not quant:
        return text
```
The next part is `apply_quant`. This function applies quantifiers to text elements, determining how many times to repeat a character or group. If no quantifier is provided, it simply returns the original text without any repetition. The function sets a foundation for handling different types of quantifiers that follow.

```python
    if quant == '*':
        n = random.randint(0, max)
        return text * n
    elif quant == '+':
        n = random.randint(1, max)
        return text * n
    elif quant == '?':
        return text if random.choice([True, False]) else ""
    elif quant.startswith('{'):
        inside = quant[1:-1]
        if ',' in inside:
            parts = inside.split(',')
            if parts[1]:
                min_n = int(parts[0])
                max_n = min(int(parts[1]), max)
            else:
                min_n = int(parts[0])
                max_n = max
            n = random.randint(min_n, max_n)
        else:
            n = int(inside)
        return text * n

    return text
```
The function handles many cases: `*` (zero or more), `+` (one or more), `?` (zero or one), and `{}` which has exact or range values. If no quantifier is found, it returns the text once.  
 For the asterisk (*), it randomly repeats the text 0 to 5 times, while for plus (+), it ensures at least one repetition. The question mark (?) randomly decides whether to include the text or not.

```python
def gen_string(tokens, max=5):
    result = ""
    for type, val, quant in tokens:
        if type == 'char':
            result += apply_quant(val, quant, max)
        elif type == 'group':
            choice = random.choice(val)
            result += apply_quant(choice, quant, max)
    return result
```
The `gen_string` function creates the final string by using the tokens.  For each token, it checks whether it's a character or a group, then applies the appropriate action. For characters, it directly applies the quantifier to the value, while for groups, it first randomly selects one option from the available choices before applying the quantifier. The function builds the result string incrementally, combining all processed tokens.

```python
def trace_gen(regex, max=5):
    tokens = re(regex)
    steps = []
    res = ""
    for i, (type, val, quant) in enumerate(tokens, 1):
        if type == 'char':
            gen = apply_quant(val, quant, max)
            res += gen
            steps.append(f"{i}) char '{val}'{f' {quant}' if quant else ''} -> '{gen}' -> '{res}'")
        elif type == 'group':
            choice = random.choice(val)
            gen = apply_quant(choice, quant, max)
            res += gen
            steps.append(f"{i}) group {val}{f' {quant}' if quant else ''} -> '{choice}' -> '{gen}' -> '{res}'")
    return steps, res
```
The `trace_gen` function shows the steps used to build the string. It is very helpful for understanding how each character or group was used. It returns both the trace and the final string. At the end, the main part of the script tests three different regex expressions. It shows five outputs for each one and prints the steps that created them.

---

## **6. Conclusions**

This lab shows how regular expressions work from the inside. Instead of using a library like re in Python, we wrote a program that breaks a regex into tokens, finds quantifiers, and then uses them to generate strings. This required thinking about how groups and characters are used and how repetition is handled.

One important part of the implementation was the `apply_quant` function. It lets the program know how many times to repeat a character or group, also used `gen_string` to combine everything together and create a full result. Another useful part was the tracing function: shows what happens at each step: which group was picked, how many times a character was added, and the final result.

The outputs shown in the attached image (result.png) are examples of what the program produced. Each regular expression is tested multiple times, and different valid strings are generated each time. Under each set of outputs, there is a list of steps taken by the program to construct the string. For example, in RE 1 `(S|T)(U|V)W*Y+24`, the string "SUWWWWYY24" was made by choosing "S", "U", repeating "W" four times, repeating "Y" two times, and then adding "2" and "4". 

In RE 2, the string always starts with "L", followed by either "M" or "N", then three "O", some "P", one "Q", and either 2 or 3. The generated strings like "LMOOOPPQ2" are correct according to the pattern. The program shows that it selects each part based on logic from the parsed regex.

In RE 3, the structure starts with multiple "R", then "S", then a group value from T, U, or V, followed by "W", and finally two values from X, Y, or Z. Generated results like "RRRSUWYY" or "STWXX" are again correct.

This lab combines ideas from formal languages, string generation, and parsing algorithms. It is useful for learning how compilers and interpreters handle input and break down code into understandable parts. It also gives experience with recursive structures and dynamic programming.

---

## **7. Bibliography**

1. [Regular expression Implementation - GitHub](https://github.com/AlexandraB-C/LFA_labs/tree/main/lab4)
2. [Regular expression (GitHub-Task)](https://github.com/filpatterson/DSL_laboratory_works/blob/master/4_regular_expressions/task.md)
3. [Regular expression (Wikipedia)](https://en.wikipedia.org/wiki/Regular_expression)
4. [Regular Expressions Tutorial (RegexOne)](https://regexone.com/)
5. [Python RegEx](https://www.w3schools.com/python/python_regex.asp)
6. [Python Regular Expressions](https://developers.google.com/edu/python/regular-expressions)

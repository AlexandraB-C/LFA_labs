import random
def re(regex):
    tokens = []
    i = 0
    
    while i < len(regex):
        # check for group
        if regex[i] == '(':
            # find matching ')'
            depth = 1
            j = i + 1
            while depth > 0 and j < len(regex):
                if regex[j] == '(':
                    depth += 1
                elif regex[j] == ')':
                    depth -= 1
                j += 1
            
            # found closing parenthesis
            if depth == 0:
                # get options
                options = regex[i+1:j-1].split('|')
                
                # check for quantifiers
                if j < len(regex) and regex[j] in '{*+?':
                    if regex[j] == '{':
                        # need to find the closing brace
                        k = j + 1
                        while k < len(regex) and regex[k] != '}':
                            k += 1
                        
                        if k < len(regex):
                            quant = regex[j:k+1]
                            tokens.append(('group', options, quant))
                            i = k + 1
                        else:
                            # no closing brace found
                            tokens.append(('group', options, ''))
                            i = j
                    else:
                        # simple quantifier like * + ?
                        tokens.append(('group', options, regex[j]))
                        i = j + 1
                else:
                    # no quantifier
                    tokens.append(('group', options, ''))
                    i = j - 1
            else:
                # unmatched parenthesis, treat as literal
                tokens.append(('char', regex[i], ''))
        
        # handle regular characters
        elif regex[i].isalnum():
            char = regex[i]
            
            # check if followed by quantifier
            if i + 1 < len(regex) and regex[i+1] in '{*+?':
                if regex[i+1] == '{':
                    # find closing brace
                    j = i + 2
                    while j < len(regex) and regex[j] != '}':
                        j += 1
                    
                    if j < len(regex):
                        quant = regex[i+1:j+1]
                        tokens.append(('char', char, quant))
                        i = j
                    else:
                        tokens.append(('char', char, ''))
                else:
                    tokens.append(('char', char, regex[i+1]))
                    i += 1
            else:
                tokens.append(('char', char, ''))
        
        i += 1
    
    return tokens

# apply quantifier to text
def apply_quant(text, quant, max=5):
    if not quant:  # no quantifier
        return text
    
    if quant == '*':  # zero or more
        n = random.randint(0, max)
        return text * n
    
    elif quant == '+':  # one or more
        n = random.randint(1, max)
        return text * n
    
    elif quant == '?':  # zero or one
        return text if random.choice([True, False]) else ""
    
    elif quant.startswith('{'):  # {n} or {n,m}
        inside = quant[1:-1]
        if ',' in inside:
            parts = inside.split(',')
            if parts[1]:  # {n,m}
                min_n = int(parts[0])
                max_n = min(int(parts[1]), max)
            else:  # {n,}
                min_n = int(parts[0])
                max_n = max
            n = random.randint(min_n, max_n)
        else:  # {n}
            n = int(inside)
        
        return text * n
    
    return text  # shouldn't get here

# generate a string from tokens
def gen_string(tokens, max=5):
    result = ""
    
    for type, val, quant in tokens:
        if type == 'char':
            result += apply_quant(val, quant, max)
        
        elif type == 'group':
            # pick one of the options randomly
            choice = random.choice(val)
            result += apply_quant(choice, quant, max)
    
    return result

# trace the generation
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

regex1 = "(S|T)(U|V)W*Y+24"
regex2 = "L(M|N)O{3}P*Q(2|3)"
regex3 = "R*S(T|U|V)W(X|Y|Z){2}"

print("RE 1:", regex1)
for i in range(5):
    tokens = re(regex1)
    s = gen_string(tokens)
    print(f"  {s}")

print("\nExp generation steps:")
steps1, res1 = trace_gen(regex1)
for step in steps1:
    print(step)

print("\nRE 2:", regex2)
for i in range(5):
    tokens = re(regex2)
    s = gen_string(tokens)
    print(f"  {s}")

print("\nExp generation steps:")
steps2, res2 = trace_gen(regex2)
for step in steps2:
    print(step)

print("\nRE 3:", regex3)
for i in range(5):
    tokens = re(regex3)
    s = gen_string(tokens)
    print(f"  {s}")

print("\nExp generation steps:")
steps3, res3 = trace_gen(regex3)
for step in steps3:
    print(step)
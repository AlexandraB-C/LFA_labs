import random
def re(regex):
    tokens = []
    i = 0
    
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
            
            # found closing parenthesis
            if depth == 0:
                options = regex[i+1:j-1].split('|')
                
                # check for quantifiers
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
            else:
                # unmatched parnth, treat as literal
                tokens.append(('char', regex[i], ''))
        elif regex[i].isalnum():
            char = regex[i]
            
            # check if followed by quantifier
            if i + 1 < len(regex) and regex[i+1] in '{*+?':
                if regex[i+1] == '{':
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

# apply quantifier
def apply_quant(text, quant, max=5):
    if not quant:
        return text
    
    if quant == '*':
        n = random.randint(0, max)
        return text * n
    
    elif quant == '+':
        n = random.randint(1, max)
        return text * n
    
    elif quant == '?':
        return text if random.choice([True, False]) else ""
    
    elif quant.startswith('{'):  # {n} or {n,m}
        inside = quant[1:-1]
        if ',' in inside:
            parts = inside.split(',')
            if parts[1]:
                min_n = int(parts[0])
                max_n = min(int(parts[1]), max)
            else:  # {n,}
                min_n = int(parts[0])
                max_n = max
            n = random.randint(min_n, max_n)
        else:
            n = int(inside)
        
        return text * n
    
    return text

def gen_string(tokens, max=5):
    result = ""
    
    for type, val, quant in tokens:
        if type == 'char':
            result += apply_quant(val, quant, max)
        
        elif type == 'group':
            choice = random.choice(val)
            result += apply_quant(choice, quant, max)
    
    return result

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

def print_regex_examples(regex, num_examples=5):
    print(f"RE: {regex}")
    
    for i in range(num_examples):
        tokens = re(regex)
        s = gen_string(tokens)
        print(f"  {s}")
    
    print("\nExp generation steps:")
    steps, res = trace_gen(regex)
    for step in steps:
        print(step)
    print()

print_regex_examples(regex1)
print_regex_examples(regex2)
print_regex_examples(regex3)
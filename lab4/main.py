import random

def generate_string(rule):
    string = ""
    i = 0
    
    print(f"Generating string for rule: {rule}")
    
    while i < len(rule):
        # Case for grouped options with no quantifier after
        if rule[i] == '(' and ')' in rule[i:]:
            closing_paren = rule.find(')', i)
            next_char_idx = closing_paren + 1
            
            # Check if there's no quantifier after the closing parenthesis
            # or if we're at the end of the string
            if next_char_idx >= len(rule) or (
                rule[next_char_idx] not in ['*', '+', '?', '{']):
                
                options_str = rule[i+1:closing_paren]
                options = options_str.split('|')
                chosen = random.choice(options)
                string += chosen
                print(f"Just one occurrence from options: Adding {chosen} to string => {string}")
                i = closing_paren + 1
                
            # Case for grouped options with * (zero or more)
            elif rule[next_char_idx] == '*':
                options_str = rule[i+1:closing_paren]
                options = options_str.split('|')
                times = random.randint(0, 5)  # 0 to 5 occurrences
                
                for _ in range(times):
                    chosen = random.choice(options)
                    string += chosen
                    print(f"Zero or more occurrences from options: Adding {chosen} to string => {string}")
                    
                i = closing_paren + 2  # Skip the * too
                
            # Case for grouped options with + (one or more)
            elif rule[next_char_idx] == '+':
                options_str = rule[i+1:closing_paren]
                options = options_str.split('|')
                times = random.randint(1, 5)  # 1 to 5 occurrences
                
                for _ in range(times):
                    chosen = random.choice(options)
                    string += chosen
                    print(f"One or more occurrences from options: Adding {chosen} to string => {string}")
                    
                i = closing_paren + 2  # Skip the + too
                
            # Case for grouped options with ? (zero or one)
            elif rule[next_char_idx] == '?':
                if random.randint(0, 1) == 1:
                    options_str = rule[i+1:closing_paren]
                    options = options_str.split('|')
                    chosen = random.choice(options)
                    string += chosen
                    print(f"Zero or one occurrence from options: Adding {chosen} to string => {string}")
                    
                i = closing_paren + 2  # Skip the ? too
                
            # Case for grouped options with {n} (fixed number)
            elif rule[next_char_idx] == '{':
                closing_brace = rule.find('}', next_char_idx)
                times = int(rule[next_char_idx+1:closing_brace])
                options_str = rule[i+1:closing_paren]
                options = options_str.split('|')
                
                for _ in range(times):
                    chosen = random.choice(options)
                    string += chosen
                    print(f"Fixed occurrences from options: Adding {chosen} to string => {string}")
                    
                i = closing_brace + 1
            
            else:
                print(f"Unhandled case at position {i}: {rule[i:]}")
                i += 1
                
        # Case for single character with ? (zero or one)
        elif i < len(rule) - 1 and rule[i+1] == '?':
            if random.randint(0, 1) == 1:
                string += rule[i]
                print(f"Zero or one occurrence: Adding {rule[i]} to string => {string}")
            i += 2
            
        # Case for single character with * (zero or more)
        elif i < len(rule) - 1 and rule[i+1] == '*':
            times = random.randint(0, 5)  # 0 to 5 occurrences
            for _ in range(times):
                string += rule[i]
                print(f"Zero or more occurrences: Adding {rule[i]} to string => {string}")
            i += 2
            
        # Case for single character with + (one or more)
        elif i < len(rule) - 1 and rule[i+1] == '+':
            times = random.randint(1, 5)  # 1 to 5 occurrences
            for _ in range(times):
                string += rule[i]
                print(f"One or more occurrences: Adding {rule[i]} to string => {string}")
            i += 2
            
        # Case for single character with ^n (power notation for repetition)
        elif i < len(rule) - 2 and rule[i+1] == '^':
            j = i + 2
            num_str = ""
            while j < len(rule) and (rule[j].isdigit() or rule[j] == '*'):
                num_str += rule[j]
                j += 1
                
            if num_str == '*':
                times = random.randint(0, 5)  # 0 to 5 occurrences
            else:
                times = int(num_str)
                
            for _ in range(times):
                string += rule[i]
                print(f"Power notation repetition: Adding {rule[i]} to string => {string}")
                
            i = j
            
        # Default case - just add the character
        else:
            string += rule[i]
            print(f"Adding {rule[i]} to string => {string}")
            i += 1
            
    return string

def main():
    # Variant 4 rules
    rule1 = "(S|T)(U|V)w^* y^+ 2x"
    rule2 = "L(M|N)O^3 P^* Q(2|3)"
    rule3 = "R* S(T|U|V)w(x|y|z)^2"
    
    print(f"Final string for rule 1: {generate_string(rule1)}")
    print(f"Final string for rule 2: {generate_string(rule2)}")
    print(f"Final string for rule 3: {generate_string(rule3)}")

if __name__ == "__main__":
    main()
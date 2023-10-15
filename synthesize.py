# Function to generate new expressions using the grammar
def grow(plist):
    new_plist = list()
    for expr in plist:
        for expr2 in plist:
            # obeys the grammar of the language
            new_plist.append('(' + expr + '+' + expr2 + ')')
            new_plist.append('(' + expr + '-' + expr2 + ')')
            new_plist.append('(' + expr + '/' + expr2 + ')')
            new_plist.append('(' + expr + '*' + expr2 + ')')
    # print("grew: ", new_plist)
    return new_plist

def elim_equiv(plist):
    ans = set()
    ans_list = []
    for pred in plist:
        try:
            # catches divisions by zero
            candidate = eval(pred)
        except:
            continue
        if candidate not in ans:
            ans.add(candidate)
            ans_list.append(pred)
            # print("eq: ", pred, "cand: ", candidate)
    return ans_list


# Main synthesis function
def synthesize(input, output):
    # Syhtesize arithmatic expression
    if isinstance(output, int):
        # convert to string
        plist = [str(ele) for ele in input]

        # Create variable encoder
        vars, d = set(), {}
        for ele in plist:
            if ele not in vars:
                vars.add(ele)
                d[ele] = chr(96 + len(vars))
        print(d)

        while True:
            plist = grow(plist)
            plist = elim_equiv(plist)
            # print("after: ", plist)
            for p in plist:
                if eval(p) == output:
                    # parse into variables
                    ans = ""
                    for char in list(p):
                        try:
                            print("trying")
                            print(d[str(int(char))])
                            ans += d[str(int(char))]
                        except:
                            ans += char
                    return ans
    else:
        # TODO: IMPLEMENT THIS PORTION
        pass

# Example inputs and outputs
input = [1, 2, 4, 7]  # Example inputs
output = 21     # Example desired output

# Synthesize a program
result = synthesize(input, output)
print("Synthesized program:", result)
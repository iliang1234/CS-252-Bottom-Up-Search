from collections import Counter
import ast
import re
import json
import pdb

# Function to generate new expressions using the grammar
def grow_arith(plist):
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

def grow_list(plist, answer):
    new_plist = plist.copy()

    for i in range(len(plist)):
        expr = plist[i]
        for j in range(len(plist)):
            expr2 = plist[j]
            # obeys the grammar of the language
            if isinstance(expr, list) and isinstance(expr2, list):
                new_plist.append('([' + ', '.join(str(i) for i in expr) + '] + [' + ', '.join(str(i) for i in expr2) + '])') # 'append'
            elif isinstance(expr, list) and isinstance(expr2, str):
                new_plist.append('([' + ', '.join(str(i) for i in expr) + '] + ' + expr2 + ')')
            elif isinstance(expr, str) and isinstance(expr2, list):
                new_plist.append('(' + expr + ' + [' + ', '.join(str(i) for i in expr2) + '])')
            else:
               new_plist.append('(' + expr + ' + ' + expr2 + ')')
            
            # evaluation
            if (expr in plist) and (expr2 in plist):
                answer.append(answer[plist.index(expr)] + answer[plist.index(expr2)])
            elif (expr in plist) and (expr2 not in plist):
                answer.append(answer[plist.index(expr)] + ast.literal_eval(expr2))
            elif (expr not in plist) and (expr2 in plist):
                answer.append(ast.literal_eval(expr) + answer[plist.index(expr2)])
            else:
                answer.append(ast.literal_eval(expr) + ast.literal_eval(expr2))

    # print("grew: ", new_plist)
    return new_plist, answer

def elim_equiv_arith(plist):
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

def elim_equiv_list(plist, answer):
    ans = []
    ans_list = []

    for i in range(len(answer)): # each pred is a list that has either been appended or not
        pred = answer[i]
        if pred not in ans:
            ans.append(plist[i])
            ans_list.append(plist[i])
            # print("eq: ", pred, "cand: ", candidate)
    return ans_list


# Main synthesis function
def synthesize(input, output):
    # Syhtesize arithmatic expression
    if isinstance(output, int) or isinstance(output, float):
        # convert to string
        plist = [str(ele) for ele in input]

        # Create variable encoder
        vars, d = set(), {}
        for ele in plist:
            if ele not in vars:
                vars.add(ele)
                d[ele] = chr(96 + len(vars))
        # print(d)

        while True:
            plist = grow_arith(plist)
            plist = elim_equiv_arith(plist)
            # print("after: ", plist)
            for p in plist:
                if eval(p) == output:
                    # parse into variables
                    ans = ""
                    for char in list(p):
                        try:
                            # print("trying")
                            # print(d[str(int(char))])
                            ans += d[str(int(char))]
                        except:
                            ans += char
                    return ans
    elif isinstance(output, list):
        plist = [str(el) for el in input]
        answer_list = [el for el in input]
        # print(d)

        while True:
            plist, answer_list = grow_list(plist, answer_list)
            plist = elim_equiv_list(plist, answer_list)
            # print("after: ", plist)
            for i in range(len(answer_list)):
                answer = answer_list[i]
                # if Counter(answer) == Counter(output):
                if answer == output:
                    ans = plist[i]
                    list_matches = re.findall(r'\[.*?\]', plist[i])

                    # Convert the matched strings (lists) to actual lists
                    isolated_lists = [json.loads(match) for match in list_matches]

                    # Create variable encoder
                    vars, d = [], {}
                    for ele in isolated_lists:
                        if ele not in vars:
                            vars.append(ele)
                            d[tuple(ele)] = chr(96 + len(vars))

                    for char in isolated_lists:
                        # try:
                        #     # print("trying")
                        #     # print(d[str(int(char))])
                        #     # ans += d[tuple(char)]
                        # except:
                        #     ans += str(char)

                        ans = ans.replace(str(char), d[tuple(char)])
                    return ans
        pass
    else:
        print("Pass in a valid inputs-output pair, in int, float, or list form.")

# Example inputs and outputs
# input = [2, 4, 7]  # Example inputs
# output = 30     # Example desired output
input = [[1, 2], [3, 1]]
output = [1, 2, 1, 2, 1, 2, 3, 1, 3, 1, 1, 2]

# NOTE: appending lists looks for the fact that all the elements in inputs appear in output; order does NOT matter

# Synthesize a program
result = synthesize(input, output)
print("Synthesized program:", result)
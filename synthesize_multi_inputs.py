from collections import Counter
import ast
import re
import json

ITERATIONS = 50
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
    new_ans = answer.copy()

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
                new_ans.append(answer[plist.index(expr)] + answer[plist.index(expr2)])
            elif (expr in plist) and (expr2 not in plist):
                new_ans.append(answer[plist.index(expr)] + ast.literal_eval(expr2))
            elif (expr not in plist) and (expr2 in plist):
                new_ans.append(ast.literal_eval(expr) + answer[plist.index(expr2)])
            else:
                new_ans.append(ast.literal_eval(expr) + ast.literal_eval(expr2))

    print("grew: ", len(new_plist))
    return new_plist, new_ans

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
    new_plist = []

    for i in range(len(answer)): # each pred is a list that has either been appended or not
        pred = answer[i]
        if pred not in ans:
            ans.append(pred)
            new_plist.append(plist[i])
            # print("eq: ", pred, "cand: ", candidate)
    return new_plist, ans


# Main synthesis function
def synthesize(inputs, outputs, iters):
    # Synthesize arithmatic/list expression
    all_outputs_list = []

    for i in range(len(inputs)):
        input = inputs[i]
        output = outputs[i]
        count = 0
        iterations = iters
        
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

            while iterations > 0:
                plist = grow_arith(plist)
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
                iterations =- 1
            
            print(ans)
            return None
            # return set(ans) if len(set(ans)) != 0 else None
            
        elif isinstance(output, list):
            plist = [str(el) for el in input]
            answer_list = [el for el in input]
            outputs_cur_list = []
            # print(d)

            # while len(max(answer_list, key=len)) <= len(output): 
            while count < len(input)+1:
                print(count)
                plist, answer_list = grow_list(plist, answer_list)
                plist, answer_list = elim_equiv_list(plist, answer_list)

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
                            ans = ans.replace(str(char), d[tuple(char)])
                        
                        if ans not in outputs_cur_list:
                            outputs_cur_list.append(ans)
                count += 1
            all_outputs_list.append(outputs_cur_list)
        else:
            print("Pass in a valid inputs-output pair, in int, float, or list form.")
    
    common_element = set(all_outputs_list[0]).intersection(*all_outputs_list[1:])
    return list(common_element)[0] if common_element else None

# Example inputs and outputs
# input = [[[3, 4], [1, 2]], [[6, 7, 8], [9]]]
# output = [[3, 4, 1, 2, 1, 2, 3, 4, 3, 4], [6, 7, 8, 9, 9, 6, 7, 8, 6, 7, 8]]
input = [[2,2],[2,2]]
output = [4, 4]
iters = 50
# Test cases for lists
# input = [[[1,2],[3,4]],[[1,3]]]
# output = [[1,2,3,4], [1,3,1,3]]


# Synthesize a program
result = synthesize(input, output, iters)
print("Synthesized program:", result)
# Test cases for arithmatic


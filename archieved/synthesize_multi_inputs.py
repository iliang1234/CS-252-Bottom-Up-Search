from collections import Counter
import ast
import re
import json
# Function to generate new expressions using the grammar
def grow_arith(plist):
    new_plist = plist.copy()
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
            # if isinstance(expr, list) and isinstance(expr2, list):
            #     print('one')
            #     new_plist.append('([' + ', '.join(str(i) for i in expr) + '] + [' + ', '.join(str(i) for i in expr2) + '])') # 'append'
            # elif isinstance(expr, list) and isinstance(expr2, str):
            #     print('two')
            #     new_plist.append('([' + ', '.join(str(i) for i in expr) + '] + ' + expr2 + ')')
            # elif isinstance(expr, str) and isinstance(expr2, list):
            #     print('three')
            #     new_plist.append('(' + expr + ' + [' + ', '.join(str(i) for i in expr2) + '])')
            expr_append = '(' + expr + ' + ' + expr2 + ')'
            new_plist.append(expr_append) # append
            
            # evaluation of append
            if (expr in plist) and (expr2 in plist):
                new_ans.append(answer[plist.index(expr)] + answer[plist.index(expr2)])
            elif (expr in plist) and (expr2 not in plist):
                new_ans.append(answer[plist.index(expr)] + ast.literal_eval(expr2))
            elif (expr not in plist) and (expr2 in plist):
                new_ans.append(ast.literal_eval(expr) + answer[plist.index(expr2)])
            else:
                new_ans.append(ast.literal_eval(expr) + ast.literal_eval(expr2))

    ret_list = new_plist.copy()
    for expr in new_plist: 
        # car (head)
        expr_car = 'CAR(' + expr + ')'
        ret_list.append(expr_car)

        if expr in new_plist:
            # pdb.set_trace()
            # cover the case where we have empty list
            if (len(new_ans[new_plist.index(expr)]) == 0) or (new_ans[new_plist.index(expr)] == [[]]):
                new_ans.append([new_ans[new_plist.index(expr)]])
            else:
                new_ans.append([new_ans[new_plist.index(expr)][0]])
        else:
            if (len(new_ans[new_plist.index(expr)]) == 0) or (new_ans[new_plist.index(expr)] == [[]]):
                new_ans.append([ast.literal_eval(expr)])
            else:
                new_ans.append([ast.literal_eval(expr)[0]])

        # cdr (tail)
        expr_cdr = 'CDR(' + expr + ')'
        ret_list.append(expr_cdr)
        if expr in new_plist:
            # cover the case where we have empty list
            if (len(new_ans[new_plist.index(expr)]) == 0) or (new_ans[new_plist.index(expr)] == [[]]):
                new_ans.append([new_ans[new_plist.index(expr)]])
            else:
                new_ans.append([new_ans[new_plist.index(expr)][-1]])
        else:
            if (len(new_ans[new_plist.index(expr)]) == 0) or (new_ans[new_plist.index(expr)] == [[]]):
                new_ans.append([ast.literal_eval(expr)])
            else:
                new_ans.append([ast.literal_eval(expr)[-1]])

    # pdb.set_trace()
    # print("grew: ", len(ret_list))
    return ret_list, new_ans

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

def createDict(input, plist):
    vars, d = set(), {}
    plist = [str(ele) for ele in input]
    # Create variable encoder
    for ele in plist:
        if ele not in vars:
            vars.add(ele)
            d[ele] = chr(96 + len(vars))
    # print("d: ", d)
    return d


# Main synthesis function
def synthesize(inputs, outputs, iters):
    # Synthesize arithmetic/list expression
    all_outputs_list = []

    # Iterate through all input/output pairs
    for i in range(len(inputs)):
        input = inputs[i]
        output = outputs[i]
        count = 0
        iterations = iters
        ans = []

        if isinstance(output, int) or isinstance(output, float):
            
            plist = [str(ele) for ele in input] # convert input to string
            d = createDict(input, plist) # map numbers to variables
            
            while iterations > 0:
                plist = grow_arith(plist)
                for p in plist:
                    # Ensure valid operation
                    try:
                        if eval(p) == output:
                            # parse into variables
                            ans_item = p
                            d_keys = [int(ele) for ele in list(d.keys())]
                            d_keys.sort(reverse=True)
                            d_sorted = {str(i): d[str(i)] for i in d_keys}
                            for key, val in d_sorted.items():
                                ans_item = ans_item.replace(key, val)

                            # ans_string = ""
                            # for char in list(p):
                            #     try:
                            #         ans_string += d[str(int(char))] # print("trying") print(d[str(int(char))])
                            #     except:
                            #         ans_string += char
                            ans.append(ans_item)
                            # print("added: ", ans_item)
                    except:
                        continue
                print(ans)
                all_outputs_list.append(ans)
                iterations -= 1
            # print("all ans: ", all_outputs_list)

            
        elif isinstance(output, list):
            plist = [str(el) for el in input]
            answer_list = [el for el in input]
            outputs_cur_list = []
            # print(d)

            # while len(max(answer_list, key=len)) <= len(output): 
            while count < 2: # 2 iterations of grow
                print(count)
                plist, answer_list = grow_list(plist, answer_list)
                # plist, answer_list = elim_equiv_list(plist, answer_list)

                # print("after: ", plist)
                for i in range(len(answer_list)):
                    answer = answer_list[i]
                    # if Counter(answer) == Counter(output):
                    if answer == output:
                        ans = plist[i]
                        list_matches = re.findall(r'\[\s*[^]]*\s*\]', plist[i])

                        # Convert the matched strings (lists) to actual lists
                        isolated_lists = [json.loads(match) for match in list_matches]
                        # pdb.set_trace()

                        # Create variable encoder
                        vars, d, c = [], {}, 0
                        for ele in input:
                            if ele not in vars:
                                vars.append(ele)
                                d[tuple(ele)] = chr(97 + c) # start with 'a', and move up
                                c += 1
                        # pdb.set_trace()
                        for char in isolated_lists:
                            ans = ans.replace(str(char), d[tuple(char)])
                        
                        if ans not in outputs_cur_list:
                            outputs_cur_list.append(ans)
                count += 1
            all_outputs_list.append(outputs_cur_list)
        else:
            print("Pass in a valid inputs-output pair, in int, float, or list form.")
    
    # print(all_outputs_list)
    common_element = set(all_outputs_list[0]).intersection(*all_outputs_list[1:])
    return list(common_element)[0] if common_element else None

# Example inputs and outputs
# input = [[[3, 4], [1, 2]], [[6, 7, 8], [9]]]
# output = [[3, 4, 1, 2, 1, 2, 3, 4, 3, 4], [6, 7, 8, 9, 9, 6, 7, 8, 6, 7, 8]]
# input = [[2,3], [4, 5, 7, 21], [2, 45]]
# output = [9, 25, 2025]
# iters = 1
# input = [2, 4, 7]  # Example inputs
# output = 30     # Example desired output
# input = [[[6, 8, 0], [3, 49], []], [[9, 6], [8, 1]]]
# output = [[6, 8, 0, 49], [9, 6, 1]]

# Synthesize a program



iters = 1
# input = [[[6, 8, 0], [5], [3, 49], []], [[9, 6], [4], [8, 1]]]
# output = [[6, 8, 0, 49, 5], [9, 6, 1, 4]] # a + cdr(c) + b
input = [[2, 2], [3, 3]]
output = [4, 9]
result = synthesize(input, output, iters)
print("Synthesized program:", result)
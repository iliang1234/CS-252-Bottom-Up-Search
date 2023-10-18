from sympy import simplify
from itertools import combinations
import ast
import re

MAX_DEPTH_LIST = 2
MAX_DEPTH_ARITH = 5

class Op:
    def __init__(self, arg_count, return_type, children_types):
        self.arg_count = arg_count
        self.return_type = return_type
        self.children_types = children_types

    def __str__(self):
        return self.__class__.__name__


class Add(Op):
    def __init__(self):
        super().__init__(2, 'float', ['float', 'float'])

    def __str__(self):
        return "+"


class Sub(Op):
    def __init__(self):
        super().__init__(2, 'float', ['float', 'float'])

    def __str__(self):
        return "-"


class Mult(Op):
    def __init__(self):
        super().__init__(2, 'float', ['float', 'float'])

    def __str__(self):
        return "*"


class Div(Op):
    def __init__(self):
        super().__init__(2, 'float', ['float', 'float'])

    def __str__(self):
        return "/"

class Append():
    def __init__(self):
        self.args_count = 2
        self.return_type = list
        self.children_types = [list, list]
    def __str__(self, x, y):
        return f"({x} + {y})"
    def eval(self, x, y):
        return str(ast.literal_eval(x) + ast.literal_eval(y))

class Car():
    def __init__(self):
        self.args_count = 1
        self.return_type = list
        self.children_types = [list]
    def __str__(self, x):
        return f"CAR({x})"
    def eval(self, x):
        x = ast.literal_eval(x)
        if x == []:
            return '[]'
        else:
            return str([x[0]])

class Cdr():
    def __init__(self):
        self.args_count = 1
        self.return_type = list
        self.children_types = [list]
    def __str__(self, x):
        return f"CDR({x})"
    def eval(self, x):
        x = ast.literal_eval(x)
        if x == []:
            return '[]'
        else:
            return str([x[-1]])
    
def createDict_list(inputs):
    ret_list = []

    for input in inputs:
        inner_dict = {}
        vars = set()
        c = 0

        # Create variable encoder
        for ele in input:
            ele_string = str(ele)
            if ele_string not in vars:
                vars.add(ele_string)
                inner_dict[chr(97 + c)] = ele_string
                c += 1
        ret_list.append(inner_dict)
    # print("ret_list: ", ret_list)
    return ret_list

def init_level_1_list(dict_of_vars):
    smallest_length = float('inf')
    smallest_keys = []

    # find set of keys that appears in all input lists
    for dictionary in dict_of_vars:
        current_length = len(dictionary)
        if current_length < smallest_length:
            smallest_length = current_length
            smallest_keys = list(dictionary.keys())
    return smallest_keys

def createDicts(inputs):
    d_list = []
    for input in inputs:
        vars, d = set(), {}
        for var in input:
            if var not in vars:
                vars.add(var)
                d[str(var)] = chr(96 + len(vars))
        d_list.append(d)
    # print("list of ds: ", d_list)
    return d_list

def initProgBank(d_list):
    min_length = min(len(d) for d in d_list)
    min_dict = [d for d in d_list if len(d) == min_length]
    min_dict_vals = [list(d.values()) for d in min_dict][0]
    return min_dict_vals

def evalProg(prog, dict):
    inv_map = {v: k for k, v in dict.items()}
    mapping = str.maketrans(inv_map)
    expr = prog.translate(mapping)
    try:
        return eval(expr)
    except:
        return None

def isChildCorrect(prog, d_list, outputs):
    for i, dict in enumerate(d_list):
        inv_map = {v: k for k, v in dict.items()}
        mapping = str.maketrans(inv_map)
        # print("dict: ", dict, "mapping: ", mapping)
        expr = prog.translate(mapping)
        # print("input", prog, "expression: ", expr)
        ans = eval(expr)
        if ans != outputs[i]:
            return False
    # print("apprently correct: ", prog, d_list, outputs)
    return True

# This version of elim_equiv includes Z as terminal numbers
# def elim_equiv_arith(prog_bank):
#     simplified = set()
#     for prog in prog_bank:
#         simp_prog = simplify(prog)
#         if simp_prog.is_integer:
#             simp_prog = '+'.join(['(a/a)'] * int(simp_prog))
#         if simp_prog not in simplified:
#             simplified.add(simp_prog)
    # print("simple: ", simplified)
    # return ['(' + str(ele) +')' for ele in simplified]

def replace_integer_with_repeated_addition(match):
    num = int(match.group())
    return '+'.join(['(a/a)'] * num)

def elim_equiv_arith(prog_bank):
    simplified = set()
    for prog in prog_bank:
        simp_prog = simplify(prog)
        simp_prog_str = str(simp_prog)

        # Replace integers in the simplified string
        simp_prog_str = re.sub(r'\b\d+\b', replace_integer_with_repeated_addition, simp_prog_str)

        if simp_prog_str not in simplified:
            simplified.add(simp_prog_str)

    return ['(' + str(ele) + ')' for ele in simplified]


OPERATIONS_ARITH = [Add(), Sub(), Mult(), Div()]

# Main synthesis function
def synthesize(inputs, outputs):

    # Synthesize arithmetic expression
    if isinstance(outputs[0], int) or isinstance(outputs[0], float):
        d_list = createDicts(inputs)
        global_prog_bank = initProgBank(d_list)
        # print("bank: ", global_prog_bank)
        max_depth = MAX_DEPTH_ARITH
        while max_depth > 0:
            inner_prog_bank = []
            for op in OPERATIONS_ARITH:
                for child in combinations(global_prog_bank, op.arg_count):
                    # print("child: ", child)
                    expr = "(" +  child[0] + str(op) + child[1] + ")"
                    # print("expr: ", expr)
                    if isChildCorrect(expr, d_list, outputs):
                        return expr
                    inner_prog_bank.append(expr)
            # prune
            pruned_progs = elim_equiv_arith(inner_prog_bank)
            global_prog_bank.extend(pruned_progs)
            # add to final
            max_depth -= 1
        return None

    # Synthesize list expression
    if isinstance(outputs[0], list):
        dict_vars = createDict_list(inputs)
        dict_grow = {} # each key is var representation, values are numerical representation (num values = num inputs)
        program_bank_list = init_level_1_list(dict_vars)
        outputs = [str(lst) for lst in outputs]
        answer_list = []
        operations_list = [Append(), Car(), Cdr()]

        # initialize answer list
        for dic in dict_vars:
            for key in dic.keys():
                if key in program_bank_list:
                    if key not in dict_grow:
                        dict_grow[key] = [dic[key]]
                    else:
                        dict_grow[key].append(dic[key])

        for _ in range(MAX_DEPTH_LIST):
            for op in operations_list:
                inner_program_bank_list = []

                for child in combinations(program_bank_list, op.args_count):
                    if op.args_count == 2: # append
                        expr = op.__str__(child[0], child[1]) # str, str

                        # evaluate expr
                        for i, _ in enumerate(dict_vars):
                            seen_exprs = list(dict_grow.keys())
                            seen_ans = list(set([j for sub in list(dict_grow.values()) for j in sub]))

                            if (child[0] in seen_exprs) and (child[1] in seen_exprs):
                                if expr not in dict_grow:
                                    dict_grow[expr] = [op.eval(dict_grow[child[0]][i], dict_grow[child[1]][i])]
                                elif len(dict_grow[expr]) < len(dict_vars):
                                    dict_grow[expr].append(op.eval(dict_grow[child[0]][i], dict_grow[child[1]][i]))
                                
                                # check if expr gives us the right outputs
                                if dict_grow[expr] == outputs:
                                    return expr
                                
                                # prune (check if there are overlapping elements)
                                set1 = set(dict_grow[expr])
                                set2 = set(seen_ans)
                                # pdb.set_trace()
                                seen = (len(set1.intersection(set2)) == len(dict_vars)) # boolean

                                if not seen:
                                    inner_program_bank_list.append(expr)

                    elif op.args_count == 1: # CAR and CDR
                        expr = op.__str__(child[0]) # str

                        # evaluate expr
                        for i, dic in enumerate(dict_vars):
                            seen_exprs = list(dict_grow.keys())
                            seen_ans = list(set([j for sub in list(dict_grow.values()) for j in sub]))

                            if (child[0] in seen_exprs):
                                if expr not in dict_grow:
                                    dict_grow[expr] = [op.eval(dict_grow[child[0]][i])]
                                elif len(dict_grow[expr]) < len(dict_vars):
                                    dict_grow[expr].append(op.eval(dict_grow[child[0]][i]))
                                
                                # check if expr gives us the right outputs
                                if dict_grow[expr] == outputs:
                                    return expr
                                
                                # prune (check if there are overlapping elements)
                                set1 = set(dict_grow[expr])
                                set2 = set(seen_ans)
                                seen = (len(set1.intersection(set2)) == len(dict_vars)) # boolean

                                if not seen:
                                    inner_program_bank_list.append(expr)

                program_bank_list += inner_program_bank_list
        return None

# EXAMPLE INPUT/OUTPUT PAIRS FOR AIRTHMETIC TARGET LANGUAGE
input, output = [[2,3], [4, 5, 7, 21], [2, 45]], [9, 25, 2025]
# input, output = [[2,3], [4, 9, 7, 21], [2, 5]], [1, 5, 3]
# input, output = [[4, 9, 2352], [9, 42, 49350, 2], [2, 4, 2]], [2, 2, 2]

# EXAMPLE INPUT/OUTPUT PAIRS FOR LIST MANIPULATION TARGET LANGUAGE
# input, output = [[[6, 8, 0], [3, 49], []], [[9, 6], [8, 1]]], [[6, 8, 0, 49], [9, 6, 1]]
# input, output = [[[6, 8, 0], [5], []], [[9, 6], []]], [[], [6]] # a + cdr(c) + cdr(a+b)
# input, output = [[[6, 8, 0], [], [1, 5]], [[9, 6],  [8, 1], []]], [[6, 8, 0, 5], [9, 6]]
# input, output = [[['a', 'be'], ['cee']], [['i'], ['love', 'you']]], [['a', 'be', 'cee', 'cee'], ['i', 'love', 'you', 'you']]

result = synthesize(input, output)
print("Synthesized program:", result)
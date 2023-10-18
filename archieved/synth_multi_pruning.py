from itertools import combinations
from sympy import simplify
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


# Usage example:
OPERATIONS = [Add(), Sub(), Mult(), Div()]
# for op in OPERATIONS:
#     print(op)
#     print("arg count", op.arg_count)
#     print("return type",op.return_type)
#     print("children", op.children_types)


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
    print("apprently correct: ", prog, d_list, outputs)
    return True

def elim_equiv_arith(prog_bank):
    simplified = set()
    for prog in prog_bank:
        simp_prog = simplify(prog)
        if simp_prog not in simplified:
            simplified.add(simp_prog)
    print("simple: ", simplified)
    return ['(' + str(ele) +')' for ele in simplified]

def synthesize(inputs, outputs, iters):
    d_list = createDicts(inputs)
    global_prog_bank, vars = initProgBank(d_list), initProgBank(d_list)
    max_depth = iters
    while max_depth > 0:
        inner_prog_bank = []
        for op in OPERATIONS:
            for child in combinations(global_prog_bank, op.arg_count):
                expr = "(" +  child[0] + str(op) + child[1] + ")"
                if isChildCorrect(expr, d_list, outputs):
                    return simplify(expr)
                inner_prog_bank.append(expr)
        # prune
        pruned_progs = elim_equiv_arith(inner_prog_bank)
        global_prog_bank.extend(pruned_progs)
        print("unpruned: ",inner_prog_bank)
        print("pruned: ",pruned_progs)
        # add to final
        max_depth -= 1
    return None

input = [[2,3], [4, 5, 7, 21], [2, 45]]
output = [9, 25, 2025]
iters = 5
ans = synthesize(input, output, iters)
print("answer: ", ans)
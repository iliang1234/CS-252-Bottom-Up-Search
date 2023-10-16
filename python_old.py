from itertools import product
import string
import pdb

def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        return float('inf')
    return a / b

# List of inputs and an output
# Goal: find a formula/expression that works for all inputs/output pairs
# NOTE: the a, b, c, ... correspond to the index of the inputs. the value of a can, for example, equal the value of b, but they correspond to the 1st and 2nd indices of the inputs, respectively

inputs_all = [[2, 3, 5], [6, 4, 7, 1]]
outputs_all = [1, 8] # should be a + a - b

operations = [add, subtract, multiply, divide]
operations_string = ['+', '-', '*', '/']

all_letters = [letter for letter in string.ascii_lowercase]

# Generates an (SINGLE) expression with inputs that yields the output
def generate_expression(inputs_all, outputs_all, operations, operations_string):
    exprs_all = []
    num_operations = len(operations)

    # iterate through all nested inputs
    for i in range(len(inputs_all)):
        inputs = inputs_all[i]
        output = outputs_all[i]
        num_inputs = len(inputs)
        letters = all_letters[:num_inputs] # number of variables/terminals
        exprs_cur_input = []

        for length in range(1, num_inputs + 1):
            # Generate all combinations of numbers and operations of the given length
            for indices in product(range(num_inputs), repeat=length):
                expr = []
                expr_str = []
                for i in range(length):
                    index = indices[i]
                    expr.append(inputs[index])
                    expr_str.append(letters[index])
                    if i < length - 1:
                        expr.append(operations[i % num_operations])
                        expr_str.append(operations_string[i % num_operations])
                
                # evaluate the generated expression
                result = expr[0]
                print(len(expr))
                for j in range(1, len(expr), 2):
                    result = expr[j](result, expr[j+1])
                
                if result == output:
                    exprs_cur_input.append(' '.join(expr_str))
                    # return (f"{expr_str} = {result}")
        exprs_all.append(exprs_cur_input)
    
    # after calculating matching expressions for all inputs/output pair (in variable form), we find an expression that appears in all pairs
    common_element = set(exprs_all[0]).intersection(*exprs_all[1:])
    return list(common_element)[0] if common_element else None

# Evaluate and display the expressions
expression = generate_expression(inputs_all, outputs_all, operations, operations_string)

print('Generated expression:')
print(expression)
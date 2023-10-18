import unittest
import re
from synthesize_multi_inputs import synthesize

def arith_decoder(candidate, input):
    # Create a dictionary to map input values to lowercase letters consistently
    input_map = {}
    next_letter = 'a'
    for val in input:
        if val not in input_map:
            input_map[val] = next_letter
            next_letter = chr(ord(next_letter) + 1)

    # Replace the lowercase letters in the candidate string with their corresponding values
    for var, val in input_map.items():
        candidate = candidate.replace(val, str(var))
    # Use eval to calculate the result of the expression
    result = eval(candidate)
    return result


class TestArithmeticProgramSynthesis(unittest.TestCase):
    def test_addition(self):
        # Define the test inputs and expected output
        iters = 1
        input = [[2,3], [4, 5, 7, 21], [2, 45]]
        output = [9, 25, 2025]

        # Call the function to get the actual output
        candidate = synthesize(input, output, iters)
        for i, ans in enumerate(output):
            self.assertEqual(arith_decoder(candidate, input[i]), ans)
        iters = 5
        input = [[2,4], [8, 4, 2, 6], [2, 2]]
        output = [9, 25, 2025]

        # Call the function to get the actual output
        candidate = synthesize(input, output, iters)
        for i, ans in enumerate(output):
            self.assertEqual(arith_decoder(candidate, input[i]), ans)

# def list_decoder(candidate, input):
#     # Define a regular expression pattern to match CDR and CAR operations
#     pattern = r'(CDR|CAR)\(([^()]*)\)'

#     # Define a replacement function to apply the CDR and CAR functions
#     def replace_match(match):
#         operation = match.group(1)
#         lst_str = match.group(2)
        
#         if operation == 'CDR':
#             return cdr(lst_str)
#         elif operation == 'CAR':
#             return car(lst_str)
#         else:
#             return ""

#     def cdr(lst_str):
#         # Get the tail of the list
#         # Remove the first character (open parenthesis) and the last character (close parenthesis)
#         lst_str = lst_str[1:-1]
#         lst = eval(lst_str)
#         return str(lst[1:]) if len(lst) > 1 else "[]"

#     def car(lst_str):
#         # Get the head of the list
#         # Remove the first character (open parenthesis) and the last character (close parenthesis)
#         lst_str = lst_str[1:-1]
#         lst = eval(lst_str)
#         return str(lst[0]) if len(lst) > 0 else "[]"

#     # Use re.sub() to replace CDR and CAR with their corresponding functions
#     decoded_candidate = re.sub(pattern, replace_match, candidate)

#     # Evaluate the decoded_candidate
#     try:
#         result = eval(decoded_candidate)
#     except:
#         # Handle any exceptions here (e.g., invalid operations)
#         result = None

#     return result



# class TestListProgramSynthesis(unittest.TestCase):
#     def test_addition(self):
#         # Define the test inputs and expected output
#         iters = 1
#         input = [[[6, 8, 0], [3, 49], []], [[9, 6], [8, 1]]]
#         output = [[6, 8, 0, 49], [9, 6, 1]]

#         # Call the function to get the actual output
#         candidate = synthesize(input, output, iters)
#         for i, ans in enumerate(output):
#             self.assertEqual(list_decoder(candidate, input[i]), ans)


if __name__ == '__main__':
    
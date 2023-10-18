# CS-252-Bottom-Up-Search

The code from this assignment is in `synthesize_FINAL.py`. <br>

The two domain language we chose to implement are arithmetic operations (+, -, *, /) and list manipulations (append, car, cdr). For operations CAR and CDR, we modify it slightly to return a list. For example, calling CAR on a list returns a list that contains its first element, and calling CDR on a list returns a list that contains its last element. <br>

The program takes in an `inputs` list and `outputs` list. The distinction between whether the program performs arithmetic operations or list manipulation depends on the type of the first element of `output`. If the type is integer or float, then the program does arithmetic program synthesis. If the type is list, then the program does list manipulation synthesis. Some sample `inputs` and `outputs` lists are as follows, as well as the synthesized program that is outputted by the algorithm: <br>

```
inputs_arith = [[2,3], [4, 5, 7, 21], [2, 45]]
outputs_arith = [9, 25, 2025]
Synthesized program: b**2

inputs_list_manipulation = [[['a', 'be'], ['cee']], [['i'], ['love', 'you']]]
outputs_list_manipulation = [['a', 'be', 'cee', 'cee'], ['i', 'love', 'you', 'you']]
Synthesized program: ((a + b) + CDR(b))
```

P.S. Note that the program should be run in Python3 in order to avoid any version errors of implemented/imported packages.
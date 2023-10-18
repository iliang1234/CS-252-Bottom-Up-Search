# CS-252 Bottom-Up Search Synthesis

The Python script `synthesize_FINAL.py` synthesize programs based on provided input-output pairs. It is tailored for arithmetic operations and list manipulations.

## About

The two domain languages chosen for the project are:

1. **Arithmetic Operations**: `+`, `-`, `*`, and `/`.
2. **List Manipulations**: Operations `append`, `car`, and `cdr`.

A note about the `car` and `cdr` operations: their behavior has been modified slightly. Using `car` on a list returns a *list* with its first element, while using `cdr` on a list returns a *list* with its last element.

The program's behavior is determined based on the type of the first element of the `output` list:

- If the type is `integer` or `float`, the program performs arithmetic synthesis.
- If the type is `list`, the program performs list manipulation synthesis.

### Sample Input and Output:

For arithmetic operations:
```python
inputs_arith = [[2,3], [4, 5, 7, 21], [2, 45]]
outputs_arith = [9, 25, 2025]
Synthesized program: b**2
```

For list manipulations:
```python
inputs_list_manipulation = [[['a', 'be'], ['cee']], [['i'], ['love', 'you']]]
outputs_list_manipulation = [['a', 'be', 'cee', 'cee'], ['i', 'love', 'you', 'you']]
Synthesized program: ((a + b) + CDR(b))
```

### Implementation Notes:
- The program uses depth-based traversal. For arithmetic operations, the maximum depth is set to 5 iterations. For list manipulations, this is reduced to 2 iterations, due to the increased complexity and corresponding runtime. Future iterations might explore size over depth.
- The script is designed for Python3 to prevent version-specific issues.

## Getting Started

To execute the program:

1. Ensure you have Python3 installed.
2. Navigate to the directory containing `synthesize_FINAL.py`.
3. Run the script:
   ```bash
   python3 synthesize_FINAL.py
   ```

## Code Overview

The script is divided into multiple classes and functions:

- **Classes for Operations**: `Op`, `Add`, `Sub`, `Mult`, `Div`, `Append`, `Car`, `Cdr`. These represent the various operations supported.
- **Utility Functions**: `createDict_list`, `init_level_1_list`, `createDicts`, `initProgBank`, `evalProg`, `isChildCorrect`, `elim_equiv_arith`. These functions provide supporting functionalities.
- **Main Synthesis Function**: `synthesize`. This is where the core logic for program synthesis resides.
- **Main Function Call**: The `synthesize` function is called on line 308. Please feel free to comment/uncomment/and add input-output test cases to explore the programs.

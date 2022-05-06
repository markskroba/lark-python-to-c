# Lark Python to C (OTCC) Translator

## Requirements

```
# lark
pip install lark
# tcc - to compile and run translated code
# should be in linux repos, "brew" for mac, or from [here](https://bellard.org/tcc/)
```

## Usage

```
python main.py <filename> tree|translate <output_filename>
```

`<filename>` - relative path to the file that should be translated
`tree` prints the 'pretty' version of a input file tree
`translate` translates code from input file (Python) to the TCC Subset, with some limitations
`<output_filename>` - if specified, the result will be written to the file at the specified path. If not it will be printed to the terminal instead

## Documentation

The goal was to get as close as possible to translating Python to [C Subset Definition for OTCC](https://bellard.org/tcc/) that OTCC and TCC support. Allowed python syntax includes:

- Declaring and assigning values to int variables
- Printing to the terminal just string and variables using `format()`
- `if/elif/else` statements
- `for/while` loops, `break`
- Function declarations with or withour parameters, `return`

## Limitations

- Variables
  - According to [C Subset Definition for OTCC](https://bellard.org/tcc/), variables cannot be initialized in declarations. Because of that, assigning 0 to a variable will be translated as declaring it.
  ```
  i = 0
  j = k = l = 0
  # will be translated to
  int i;
  int j,k,l;
  ```

* Printing
  - There are two main ways of using `print()` - passing string to it, or passing string with `format()` method to it to embed variables
  ```
    print("Hello world, its 10 AM")
    print("Hello, world, its {} AM".format(10))
    print("Hello, world, its {} AM".format(time()))
    # will be translated to
    printf("Hello world, its 10 AM");
    printf("Hello world, its {%i} AM", hour())
    # all will be printed the same
  ```

- For-loops
  - `range()` should be used to define how many iterations will occur

* Function declaration
  - `if __name__="__main__":` will be translated to `int main(){ }`
  * Since it seems that `return`-statements is not always required (even for `main()`), it will be added only it was present in the Python code

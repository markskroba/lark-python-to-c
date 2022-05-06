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
- For-loops
  - `range()` should be used to define how many iterations will occur

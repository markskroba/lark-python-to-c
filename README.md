# Lark Python to C (TCC) Translator

[from Obfuscated Tiny C Compiler, C Subset Definition](https://bellard.org/otcc/)

* Expressions:
    * binary operators, by decreasing priority order: ~~'*' '/' '%', '+' '-',~~ '>>' '<<', '<' '<=' '>' '>=', '==' '!=', '&', '^', '|', '=', '&&', '||'.
    * '&&' and '||' have the same semantics as C : left to right evaluation and early exit.
    * ~~Parenthesis are supported.~~
    * Unary operators: '&', '*' (pointer indirection), '-' (negation), '+', '!', '~', post fixed '++' and '--'.
    * Pointer indirection ('*') only works with explicit cast to 'char *', 'int *' or 'int (*)()' (function pointer).
    * '++', '--', and unary '&' can only be used with variable lvalue (left value).
    * ~~'=' can only be used with variable or '*' (pointer indirection) lvalue.~~
    * Function calls are supported with standard i386 calling convention. Function pointers are supported with explicit cast. Functions can be used before being declared.
* Types: only signed integer ('int') variables and functions can be declared. Variables cannot be initialized in declarations. Only old K&R function declarations are parsed (implicit integer return value and no types on arguments).
* ~~Any function or variable from the libc can be used because OTCC uses the libc dynamic linker to resolve undefined symbols.~~ **IGNORED**
* Instructions: ~~blocks ('{' '}') are supported as in C. 'if' and 'else' can be used for tests.~~ The 'while' and 'for' C constructs are supported for loops. 'break' can be used to exit loops. ~~'return' is used for the return value of a function.~~
* Identifiers are parsed the same way as C. Local variables are handled, but there is no local name space (not a problem if different names are used for local and global variables).
* Numbers can be entered in decimal, hexadecimal ('0x' or '0X' prefix), or octal ('0' prefix).
* '#define' is supported without function like arguments. No macro recursion is tolerated. Other preprocessor directives are ignored.
* C Strings and C character constants are supported. Only '\n', '\"', '\'' and '\\' escapes are recognized.
* C Comments can be used (but no C++ comments).
* No error is displayed if an incorrect program is given.
* ~~Memory: the code, data, and symbol sizes are limited to 100KB (it can be changed in the source code).~~ **IGNORED**
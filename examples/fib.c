#include <stdio.h>

fib(n)
{
    if (n <= 2)
        return 1;
    else
        return fib(n-1) + fib(n-2);
}

main()
{
    printf("%i\n", fib(10));
    return 0;
}
#include <stdio.h>

fact(n)
{
    int i, r;
    r = 1;
    for(i = 2; i <= n; i++)
    {
        r = r * i;
    }

    return r;
}

main()
{
    printf("%i\n", fact(10));
    return 0;
}
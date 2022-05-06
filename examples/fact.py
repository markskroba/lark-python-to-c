def fact(n):
    i = 0
    r = 0
    r = 1
    for i in range(2, n+1):
        r = r * i
        
    return r

if __name__ == "__main__":
    print("{}".format(fact(10)))
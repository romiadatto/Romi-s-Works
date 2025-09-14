def print_n_items(a, d, n):
    t_1 = a
    t_prev = t_1
    print(t_1)
    for i in range(2, n + 1):
        t_i = t_prev + d
        print(t_i)
        t_prev = t_i


def nth_item(a, d, n):
    t_n = a + (n - 1) * d
    return t_n


def sum_n_items(a, d, n):
    S_n = (n / 2) * (2 * a + (n - 1) * d)
    print("Sum of first n terms:",S_n)

def sum_n_odd_items(a,d,n):
    print("the numbers in the odd places: ")
    for i in range(a,n,d):
        if(i%2==0):
            print(i,", ", end="")

def solution(arg):
    transactions = 0
    for i in range(len(arg)):
        total = 0
        for j in range(i, len(arg)):
            total += arg[j]
            if total == 0:
                transactions += 1
    print(transactions)

array = [1, 1, 2, -3, 0, 1000, 6, -6, 1, 1, 1, -3, 2]
solution(array)
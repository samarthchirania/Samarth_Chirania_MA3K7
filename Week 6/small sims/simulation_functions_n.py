import random

def simulate(n):
    numbers = list(range(1, n + 1))
    while len(numbers) > 1:
        a, b = random.sample(numbers, 2)
        numbers.remove(a)
        numbers.remove(b)
        diff = abs(a - b)

        numbers.append(diff)
    return numbers[0]

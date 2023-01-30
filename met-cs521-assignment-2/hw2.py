# Tomas Hornicek, no collaborators,https://developer.mozilla.org/en-US/, https://www.w3schools.com/,no extension
import random


# Determines whether a year is a leap year
def is_leap(year):
    if (year % 4 == 0) and (year % 100 != 0):
        return True
    elif (year % 100 == 0) and (year % 400 == 0):
        return True
    else:
        return False


print(is_leap(2020))
print(is_leap(2001))
print(is_leap(2005))


# Determines whether a number is a triangular number
def is_triangle(num):
    sum = 0
    n = 1
    while sum <= num:
        sum = sum + n
        if sum == num:
            return True
        n += 1
    return False


print(is_triangle(10))


# Determine the triangular sum, given lower and upper bound
def triangle_sum(lower_bound, upper_bound):
    tri_range = range(lower_bound, upper_bound + 1)
    # print(tri_range)
    tri_list = list(tri_range)
    sum = 0
    for i in tri_list:
        if is_triangle(i):
            # print(i)
            sum += i
    return sum


print(triangle_sum(1, 10))
print(triangle_sum(10, 20))


# Generate a list of n random numbers(1-9)
def random_gen(n):
    random_list = list()
    for i in range(n):
        randomNumber = random.randint(1, 9)
        random_list.append(randomNumber)
    return random_list


print(random_gen(100))


# Determine sum of two binary numbers, answer in decimal
def bit_and(a, b):
    bit_list = list()
    a_list = list(a)
    b_list = list(b)
    length_a = len(a)
    length_b = len(b)
    if length_a > length_b:
        difference = length_a - length_b
        a_list = a_list[difference:]
    elif length_b > length_a:
        difference = length_b - length_a
        b_list = b_list[difference:]
    for i in range(len(a_list)):
        if a_list[i] == b_list[i] and a_list[i] == "1":
            bit_list.append(1)
        else:
            bit_list.append(0)
    sum = 0
    for index, value in enumerate(bit_list):
        if value == 1:
            power_of_two = len(bit_list) - index - 1
            number_add = 2 ** power_of_two
            sum += number_add
    return sum


print(bit_and("1011", "10"))


# Determine the sum of given numbers
def digit_sum(num):
    sum = 0
    while num:
        sum += num % 10
        num //= 10
    return sum


print(digit_sum(129))

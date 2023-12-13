
def sum_of_n_formula(n):
    return n * (n + 1) // 2

num_natural_numbers = int(input("Enter the value of n for the sum of first n natural numbers: "))

result_formula = sum_of_n_formula(num_natural_numbers)
print(f"Sum using formula: {result_formula}")


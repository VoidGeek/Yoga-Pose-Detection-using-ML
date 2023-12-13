def generate_asterisks(arr):
    for element in arr:
        if isinstance(element, int) and element >= 0:
            print('*' * element)
        else:
            print("Invalid input. Please provide a non-negative integer.")

input_str = input("Enter a list of non-negative integers separated by spaces: ")
input_array = [int(x) for x in input_str.split()]

generate_asterisks(input_array)

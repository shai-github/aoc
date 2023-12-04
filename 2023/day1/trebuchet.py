import re


def read_data(pathname: str) -> str:
    """
    Reads data from a file and returns it as a string
    :param pathname: The path to the file
    :return: The data as a string
    """
    with open(pathname) as f:
        return f.read()


def parse_data(data_string: str) -> list:
    """
    Splits the data string into a list of lines
    :param data_string: The data as a string
    :return: The data as a list of lines
    """
    return data_string.split("\n")


def find_numbers(data: list):
    """
    Retrieve all numbers from the data as a list of lists of digits
    :param data: The data as a list of lines
    :return: The numbers as a list of lists of digits
    """
    ret_list = []
    all_numbers = [[num for num in re.findall(r"\d+", line)] for line in data]
    
    for numbers in all_numbers:
        separated_numbers = []
        for number in numbers:
            separated_numbers += [digit for digit in number]
        ret_list.append(separated_numbers)

    return ret_list


def merge_digit_pairs(digits: list):
    """
    Merge the first and last digits of each number into a list of pairs
        If there is only one digit, the pair is the same digit twice
    :param digits: The numbers as a list of lists of digits
    :return: The pairs as a list of integers
    """
    digit_pairs = []

    for digit_list in digits:
        if len(digit_list) == 1:
            digit_pairs.append(int(digit_list[0] + digit_list[0]))
        else:
            digit_pairs.append(int(digit_list[0] + digit_list[-1]))

    return digit_pairs


def main():
    """
    """
    data = parse_data(
        data_string=read_data(pathname="input.txt")
    )

    digits = find_numbers(data=data)
    pairs = merge_digit_pairs(digits=digits)

    return sum(pairs)

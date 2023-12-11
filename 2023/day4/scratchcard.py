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


def split_numbers(data: list) -> dict:
    """
    """
    return {
        idx: {
            'win': [elem for elem in re.split(r'(\s)', line.split(": ")[1].split(" | ")[0]) if elem not in [' ', '']],
            'card': [elem for elem in re.split(r'(\s)', line.split(": ")[1].split(" | ")[1]) if elem not in [' ', '']]
        } for idx, line in enumerate(data)
    }


def sum_points():
    """
    """
    data = parse_data(read_data("input.txt"))
    split = split_numbers(data)
    
    print(data[0])
    print(split[0])

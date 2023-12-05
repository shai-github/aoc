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


def get_number_spans(data: list) -> dict:
    """
    Gets the index spans of all numbers in a line
    :param data: The data as a list of lines
    :return: a dictionary mapping a line index to the positional spans 
        of numbers in a given line
    """


def get_symbol_indices(data: list) -> dict:
    """
    Gets the index of all symbols in a line
    :param data: The data as a list of lines
    :return: a dictionary mapping a line index to the positions of symbols
        in a given line
    """


def scan_lines(data: list) -> dict:
    """
    Scans the lines in the input data for numbers and symbols
    :param data: The data as a list of lines
    :return: a dictionary mapping a line index to the positions of numbers
        and symbols in a given line
    """



def sum_adjacent():
    """
    Sums the numbers that are adjacent to a symbol according to the 
        criteria specified in part 1
    """
    data = parse_data(read_data("input.txt"))

    return data
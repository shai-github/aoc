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
    Splits the data into a dictionary of lines with the numbers split out
    :param data: The data as a list of lines
    :return: The data as a dictionary of lines with the numbers split out
        for winning numbers and actual card numberes for a given card
    """
    return {
        idx: {
            'win': [elem for elem in re.split(r'(\s)', line.split(": ")[1].split(" | ")[0]) if elem not in [' ', '']],
            'card': [elem for elem in re.split(r'(\s)', line.split(": ")[1].split(" | ")[1]) if elem not in [' ', '']]
        } for idx, line in enumerate(data)
    }


def score_cards(data: list) -> list:
    """
    Scores the cards based on the winning numbers and the card numbers
    :param data: The data as a list of lines
    :return: a list of scores for each card
    """
    card_data = split_numbers(data=data)
    points = {idx: 0 for idx in card_data.keys()}

    for idx, card in card_data.items():
        wins = [int(num) for num in card['card'] if num in card['win']]
        if len(wins) == 0:
            continue
        elif len(wins) == 1:
            points[idx] = 1
        elif len(wins) > 1:
            points[idx] = 2**(len(wins)-1)
    
    return [score for score in points.values()]


def sum_points():
    """

    """
    data = parse_data(read_data("input.txt"))
    score_list = score_cards(data=data)

    return sum(score_list)

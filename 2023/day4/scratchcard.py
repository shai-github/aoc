import re

from collections import defaultdict


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
    points = {
        idx: {
            'score': 0,
            'matches': 0
        } for idx in card_data.keys()
    }

    for idx, card in card_data.items():
        wins = [int(num) for num in card['card'] if num in card['win']]
        if len(wins) == 0:
            continue
        elif len(wins) == 1:
            points[idx]['score'] = 1
            points[idx]['matches'] = 1
        elif len(wins) > 1:
            points[idx]['score'] = 2**(len(wins)-1)
            points[idx]['matches'] = len(wins)
    
    return points


def copy_cards(points: dict) -> list:
    """
    Sums the number of cards that meet the matching criteria
        for part 2 of the challenge
    :param points: The dictionary of scores and matches for each card
    :return: The number of cards that meet the matching criteria
    """
    card_map = defaultdict(int)

    for idx, score in points.items():
        card_map[idx] += 1
        for count in range(idx + 1, min(idx + 1 + score['matches'], len(points))):
            card_map[count] += card_map[idx]

    return sum([count for count in card_map.values()])


def sum_points(copy_bool: bool = False) -> int:
    """
    Sums points or card copies based on the copy_bool flag
    :param copy_bool: A flag to determine whether to sum points or card copies
    :return: The sum of points or card copies
    """
    data = parse_data(read_data("input.txt"))
    points = score_cards(data=data)

    if copy_bool:
        return copy_cards(points=points)

    return sum([score['score'] for score in points.values()])


if __name__ == "__main__":
    print(f"The sum of all card scores for part 1 is {sum_points()}")
    print(f"The sum of all card scores for part 2 is {sum_points(copy_bool=True)}")

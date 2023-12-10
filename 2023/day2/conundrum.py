import re
import operator

from functools import reduce


CUBE_MAP = {
    "red": 12,
    "green": 13,
    "blue": 14,
}


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


def map_color_games(data: list) -> dict:
    """
    Maps the color sets to their corresponding numbers
    :param data: The data as a list of lines
    :return: A dictionary mapping a game to the number of colors 
    """
    count_map = {
        int(idx + 1): {
            game: [element for element in game_list.replace(",", "").split(" ") if element != ""]
            for game, game_list in enumerate(re.sub(r'^.*?:', ':', line)[2:].split(";"))
        } for idx, line in enumerate(data)
    }

    return {
        game: {
            num: {
                'count': [elem for pos, elem in enumerate(game_count) if pos % 2 == 0],
                'color': [elem for pos, elem in enumerate(game_count) if pos % 2 != 0]
            } for num, game_count in counts.items()
        } for game, counts in count_map.items()
    }


def filter_games(color_games: dict, filter: bool = False) -> list:
    """
    Filters for the games that meet the criteria
    :param color_games: The games mapped to their color counts
    :param filter: Whether or not to filter the games by part 1 criteria
        if False, filter to get the minimum number needed of each color
    :return: A sum of indices of games that meet the criteria
    """
    ret_list = []

    for game, counts in color_games.items():
        if filter:
            fails_check = False
        else:
            map_dict = {color: 0 for color in CUBE_MAP.keys()}
        for data in counts.values():
            if filter:
                for pos, color in enumerate(data['color']):
                    if CUBE_MAP[color] < int(data['count'][pos]):
                        fails_check = True
            else:
                for pos, color in enumerate(data['color']):
                    if int(data['count'][pos]) > map_dict[color]:
                        map_dict[color] = int(data['count'][pos])
        if filter:
            if not fails_check:
                ret_list.append(game)
        else:
            val = list(map_dict.values())
            ret_list.append(reduce(operator.mul, val, 1))
                    
    return sum(ret_list)


def sum_ids(filter: bool = False):
    """
    Sums the indices of the games that meet the criteria for part 1 or 2
    :return: The sum of the indices of the games that meet the criteria
    """
    data = parse_data(read_data("input.txt"))
    color_games = map_color_games(data)

    return filter_games(color_games=color_games, filter=filter)


if __name__ == "__main__":
    print(f"The sum of the indices of the games that meet the criteria is {sum_ids(filter=True)}")
    print(f"The sum of the power of minimum colors for all games is {sum_ids()}")
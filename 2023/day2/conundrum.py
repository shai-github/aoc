import re


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


def filter_games(color_games: dict) -> list:
    """
    Filters for the games that meet the criteria
    :param color_games: The games mapped to their color counts
    :return: A sum of indices of games that meet the criteria
    """
    ret_list = []

    for game, counts in color_games.items():
        fails_check = False
        for data in counts.values():
            for pos, color in enumerate(data['color']):
                if CUBE_MAP[color] < int(data['count'][pos]):
                    fails_check = True
        if not fails_check:
            ret_list.append(game)
                    
    return sum(ret_list)


def sum_ids():
    """
    Sums the indices of the games that meet the criteria
    :return: The sum of the indices of the games that meet the criteria
    """
    data = parse_data(read_data("input.txt"))
    color_games = map_color_games(data)

    return filter_games(color_games)


if __name__ == "__main__":
    print(sum_ids())
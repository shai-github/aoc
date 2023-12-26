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


def map_data(data: list) -> dict:
    """
    Maps the data into a dictionary format
    :param data: The data as a list of lines
    :return: The data split out into items for seeds, seed-to-soil map, 
        soil-to-fertilizer map, fertilizer-to-water map, water-to-light map,
        light-to-temperature map, temperature-to-humidity map, and
        humidity-to-location map
    """
    data_map = defaultdict()
    data_breaks = [idx + 1 for idx, line in enumerate(data) if line == ""]

    for idx, line in enumerate(data):
        if idx == 0:
            data_map["seeds"] = line.replace("seeds: ", "").split(" ")
        elif idx in data_breaks:
            db_next = data_breaks.index(idx) + 1
            if db_next == len(data_breaks):
                ref_data = data[idx + 1:]
            else:
                ref_data = data[idx + 1: data_breaks[db_next]]

            data_map[data[idx].replace(":", "")] = [line.split(" ") for line in ref_data if line != ""]
    
    return data_map
    

def something():
    """
    """
    data = parse_data(read_data("input.txt"))
    data_map = map_data(data=data)

    return data_map


if __name__ == "__main__":
    pass
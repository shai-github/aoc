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
            string_num = line.replace("seeds: ", "").split(" ")
            data_map["seeds"] = [int(num) for num in string_num]
        elif idx in data_breaks:
            db_next = data_breaks.index(idx) + 1
            if db_next == len(data_breaks):
                ref_data = data[idx + 1:]
            else:
                ref_data = data[idx + 1: data_breaks[db_next]]

            string_num = [line.split(" ") for line in ref_data if line != ""]
            data_map[data[idx].replace(":", "")] = [[int(num) for num in line] for line in string_num]
    
    return data_map
    

def pair_mapping(num_list: list) -> dict:
    """
    Maps destination range starts to source range start according to
        a given range length. 
    :param num_list: The list of numbers to map
    :return: The mapping of destination range starts to source range starts
    """
    num_map = defaultdict()

    for mapping in num_list:
        num_map[mapping[0]] = {
            "source": [mapping[1], mapping[1] + mapping[2]-1],
            "range": mapping[2]
        }

    return num_map


def make_mappings(data_map: dict) -> dict:
    """
    Calculate the mappings for each of the data types. Order matters
        for the final mappings of seeds to location, so the order of
        the input data is mapped according to index.
    :param data_map: The input data as a dictionary
    :return: The mappings for each of the data types
    """
    return {
        idx: pair_mapping(num_list=val) for idx, val in enumerate(data_map.values())
    }


def traverse_mappings(seeds: list, mappings: dict) -> dict:
    """
    Traverses the mappings for seeds to soil, soil to fertilizer,
        fertilizer to water, water to light, light to temperature,
        temperature to humidity, and humidity to location.
    :param seeds: The seeds to map
    :param mappings: The mappings for each of the data types
    :return: The mapping of seeds to location
    """
    location_map = defaultdict()

    for seed in seeds:
        for idx, mapping in mappings.items():
            valid_map = False
            if idx == 0:
                ref = seed
            for key, val in mapping.items():
                if val["source"][0] <= ref <= val["source"][1]:
                    ref = (ref - val["source"][0]) + key
                    valid_map = True
                    break
            if not valid_map:
                ref = ref
        location_map[seed] = ref

    return location_map


def find_minimum():
    """
    Retrieves the minimum location value from mapping the seeds to
        locations via the mappings for seeds to soil, soil to fertilizer,
        fertilizer to water, water to light, light to temperature,
        temperature to humidity, and humidity to location.
    :return: The minimum location value
    """
    data_map = map_data(data=parse_data(read_data("input.txt")))
    mappings = make_mappings(
        data_map={k: v for k, v in data_map.items() if k != "seeds"}
    )

    location_map = traverse_mappings(
        seeds=data_map["seeds"], 
        mappings=mappings
    )

    return min(location_map.values())


if __name__ == "__main__":
    print("The minimum location value is:", find_minimum())
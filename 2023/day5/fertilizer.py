from collections import defaultdict
import time

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


def map_data(data: list, use_range: bool = False) -> dict:
    """
    Maps the data into a dictionary format
    :param data: The data as a list of lines
    :param use_range: Whether to use the range of values for seeds
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
            int_list = [int(num) for num in string_num]
            if use_range:
                data_map["seeds"] = list(zip(int_list[0::2], int_list[1::2]))
            else:
                data_map["seeds"] = int_list
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


def traverse_by_seed(seeds: list, mappings: dict) -> dict:
    """
    Traverses the mappings for individuals seeds to soil, soil to fertilizer,
        fertilizer to water, water to light, light to temperature,
        temperature to humidity, and humidity to location.
    :param seeds: The seeds to map
    :param mappings: The mappings for each of the data types
    :param use_range: Whether to use the range of values for seeds
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


def traverse_by_range(seeds: list, mappings: dict) -> dict:
    """
    Traverses the mappings for seed ranges to soil, soil to fertilizer,
        fertilizer to water, water to light, light to temperature,
        temperature to humidity, and humidity to location.
    :param seeds: The seeds to map
    :param mappings: The mappings for each of the data types
    :param use_range: Whether to use the range of values for seeds
    :return: a list of seeds
    """
    reduced_mappings = []

    for mapping in mappings.values():
        for destination, source in mapping.items():
            reduced_mappings.append([destination, source["source"][0], source["range"]])

    


    # print(map_list)
    locations = []

    for seed_range in seeds:
        seed_range.append((seed_range[0] + seed_range[1] - 1))
        range_ref = [seed_range]
        next_pass = []

        while range_ref:
            ref = range_ref.pop()
            for _, mapping in mappings.items():
                for destination, source in mapping.items():
                    if (ref[0] > source["source"][1]) or (ref[2] < source["source"][0]):
                        continue
                    elif source["source"][1] > ref[2] >= ref[0] >= source["source"][0]:
                        delta = ref[0] - source["source"][0]





                    if seed_range[0] > source["source"][1]:
                        continue
                    elif (seed_range[0] >= source["source"][0]) and (seed_range[0] <= source["source"][1]):
                        if (seed_range[0] + seed_range[1] - 1) <= source["source"][1]:
                            next_pass.append(((seed_range[0] + destination - source["source"][0]), seed_range[1]))
                        elif (seed_range[0] + seed_range[1] - 1) > source["source"][1]:
                            range_delta = (seed_range[0] + seed_range[1] - 1) - source["source"][1]
                            next_pass.append(
                                (seed_range[0] + destination, source["source"][1] - seed_range[0] + 1), 
                            )
                            range_ref.append((source["source"][1] + 1, range_delta))
                        break
                    elif seed_range[0] < source["source"][0]:
                        if (seed_range[0] + seed_range[1] - 1) < source["source"][0]:
                            continue
                        else:
                            range_delta = source["source"][0] - seed_range[0]
                            if (seed_range[0] + seed_range[1] - 1) <= source["source"][1]:
                                next_pass.append( 
                                    ((seed_range[0] + range_delta + destination), ((seed_range[0] + seed_range[1] - 1) - source["source"][0]))
                                )
                                range_ref.append((seed_range[0], range_delta))
                            elif (seed_range[0] + seed_range[1] - 1) > source["source"][1]:
                                post_range = (seed_range[0] + seed_range[1] - 1) - source["source"][1]
                                next_pass.append(
                                    ((seed_range[0] + range_delta + destination), ((seed_range[0] + seed_range[1] - 1) - source["source"][0]))
                                )
                                range_ref.append((seed_range[0], range_delta))
                                range_ref.append((source["source"][1], post_range))
                        break
                else:
                    range_ref.append(ref)
        range_ref = next_pass
        next_pass = []

    locations.extend(range_ref)
    print(locations)

    range_set = set(range_ref)
    return min([r[0] for r in range_set])


def find_minimum(use_range: bool = False):
    """
    Retrieves the minimum location value from mapping the seeds to
        locations via the mappings for seeds to soil, soil to fertilizer,
        fertilizer to water, water to light, light to temperature,
        temperature to humidity, and humidity to location.
    :param use_range: Whether to use the range of values for seeds
    :return: The minimum location value
    """
    data_map = map_data(
        data=parse_data(read_data("test.txt")),
        use_range=use_range
    )

    mappings = make_mappings(
        data_map={k: v for k, v in data_map.items() if k != "seeds"}
    )

    if use_range:
        return traverse_by_range(
            seeds=data_map["seeds"], 
            mappings=mappings,
        )

    location_map = traverse_by_seed(
        seeds=data_map["seeds"], 
        mappings=mappings,
    )

    return min(location_map.values())


if __name__ == "__main__":
    print("The minimum location value for seeds only is:", find_minimum())
    print("The minimum location value for seed ranges is:", find_minimum(use_range=True))
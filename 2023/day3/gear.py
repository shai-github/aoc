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


def get_number_spans(line: list) -> dict:
    """
    Gets the index spans of all numbers in a line
    :param line: line of input data
    :return: a dictionary mapping a line index to the positional spans 
        of numbers in a given line
    """
    ref_int = 0
    ret_dict = defaultdict()

    ref_dict = {
        idx: num for idx, num in enumerate(line) if num.isdigit()
    }

    for idx, key in enumerate(ref_dict.keys()):
        if idx == 0:
            ret_dict[ref_int] = {
                'number': ref_dict[key],
                'pos': [key]
            }
            last_int = key
        else:
            if key == last_int + 1:
                ret_dict[ref_int]['number'] += ref_dict[key]
                ret_dict[ref_int]['pos'].append(key)
                last_int = key
            else:
                ref_int += 1
                ret_dict[ref_int] = {
                    'number': ref_dict[key],
                    'pos': [key]
                }
                last_int = key

    return ret_dict


def get_symbol_indices(line: list, filter_gear: bool = False) -> dict:
    """
    Gets the index of all symbols in a line
    :param line: line of input data
    :param filter_gear: whether to filter for gear symbols
    :return: a dictionary mapping a line index to the positions of symbols
        in a given line
    """
    if filter_gear:
        return [idx for idx, sym in enumerate(line) if sym == "*"]
    else:
        return [idx for idx, sym in enumerate(line) if (not sym.isdigit()) and (sym != ".")]


def scan_lines(data: list, filter_gear: bool = False) -> dict:
    """
    Scans the lines in the input data for numbers and symbols
    :param data: The data as a list of lines
    :param filter_gear: whether to filter for gear symbols
    :return: a dictionary mapping a line index to the positions of numbers
        and symbols in a given line
    """
    return {
        idx: {
            'num': get_number_spans(line=line),
            'sym': get_symbol_indices(line=line, filter_gear=filter_gear)
        } for idx, line in enumerate(data)
    }


def get_gear_powers(data: list) -> list:
    """
    Gets the power of all numbers adjacent to gear symbols in a line
    :param data: The data as a list of lines
    :return: a list of gear powers
    """
    line_gears = []
    scan_data = scan_lines(data=data, filter_gear=True)
    max_key = max(scan_data.keys())

    for idx, scan in scan_data.items():
        for gear_idx in scan['sym']:
            gear_nums = []
            for num_data in scan['num'].values():
                if any(pos in num_data['pos'] for pos in [gear_idx - 1, gear_idx + 1]):
                    gear_nums.append(int(num_data['number']))
            if idx != 0:
                for num_data in scan_data[idx - 1]['num'].values():
                    if any(pos in num_data['pos'] for pos in [gear_idx - 1, gear_idx + 1, gear_idx]):
                        gear_nums.append(int(num_data['number']))
                for num_data in scan_data[idx + 1]['num'].values():
                    if any(pos in num_data['pos'] for pos in [gear_idx - 1, gear_idx + 1, gear_idx]):
                        gear_nums.append(int(num_data['number']))
            elif idx == max_key:
                for num_data in scan_data[idx - 1]['num'].values():
                    if any(pos in num_data['pos'] for pos in [gear_idx - 1, gear_idx + 1, gear_idx]):
                        gear_nums.append(int(num_data['number']))
            elif idx == 0 :
                for num_data in scan_data[idx + 1]['num'].values():
                    if any(pos in num_data['pos'] for pos in [gear_idx - 1, gear_idx + 1, gear_idx]):
                        gear_nums.append(int(num_data['number']))
            if len(gear_nums) == 2:
                line_gears.append(gear_nums[0] * gear_nums[1])

    return line_gears


def get_adjacent_numbers(data: list) -> list:
    """
    Gets the adjacent numbers to a symbol in a line
    :param data: The data as a list of lines
    :return: a list of adjacent numbers to a symbol in a line
    """
    ret_list = []
    scan_data = scan_lines(data=data)
    max_key = max(scan_data.keys())

    for idx, scan in scan_data.items():
        for num_data in scan['num'].values():
            pos_list = num_data['pos'] + [min(num_data['pos']) - 1, max(num_data['pos']) + 1]
            if any(pos in pos_list for pos in scan['sym']):
                ret_list.append(int(num_data['number']))
                continue
            if idx != 0:
                if idx == max_key:
                    if any(pos in pos_list for pos in scan_data[idx - 1]['sym']):
                        ret_list.append(int(num_data['number']))
                        continue
                else:
                    if any(pos in pos_list for pos in scan_data[idx - 1]['sym']) or any(pos in pos_list for pos in scan_data[idx + 1]['sym']):
                        ret_list.append(int(num_data['number']))
                        continue
            else:
                if any(pos in pos_list for pos in scan_data[idx + 1]['sym']):
                    ret_list.append(int(num_data['number']))
                    continue

    return ret_list
            

def sum_adjacent(filter_gear: bool = False):
    """
    Sums the numbers that are adjacent to a symbol according to the 
        criteria specified in part 1
    :param filter_gear: whether to filter for gear symbols
    :return: the sum of all numbers adjacent to a symbol given
        part 1 or part 2 criteria
    """
    data = parse_data(read_data("input.txt"))
    
    if filter_gear:
        adjacent_numbers = get_gear_powers(data=data)
    else:
        adjacent_numbers = get_adjacent_numbers(data=data)

    return sum(adjacent_numbers)


if __name__ == "__main__":
    print(f"The sum of all numbers adjacent to a symbol is {sum_adjacent()}")
    print(f"The sum of all numbers meeting gear criteria is {sum_adjacent(filter_gear=True)}")
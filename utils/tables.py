from tabulate import tabulate


def create_table_extend(data_input, locations):
    result = [[] for _ in range(len(locations))]

    for data in data_input:
        for location_idx, location in enumerate(locations):
            current_data = data
            keys = location.split(".")
            for key in keys:
                if isinstance(current_data, list):
                    new_data = []
                    for entry in current_data:
                        new_value = entry.get(key)
                        if isinstance(new_value, list):
                            new_data.extend(new_value)
                        else:
                            new_data.append(new_value)
                    current_data = new_data
                else:
                    current_data = current_data.get(key)

            if isinstance(current_data, list):
                result[location_idx].extend(current_data)
            else:
                result[location_idx].append(current_data)

    return ["\n".join(map(str, sublist)) for sublist in result]


def tabularize(list_of_unknown_type, headers, numbering=True, tablefmt="mixed_grid"):
    table = []
    table.append(headers)
    for unknown_type in list_of_unknown_type:
        if type(unknown_type) == dict:
            table.append(list(unknown_type.values()))
        if type(unknown_type) == list:
            table.append(unknown_type)

    return tabulate(
        table,
        headers="firstrow",
        tablefmt=tablefmt,
        showindex=range(1, len(list_of_unknown_type) + 1) if numbering else False,
    )

def parse_data(file_path):

    file = open(file_path, 'r')
    raw_data = file.read()
    file.close()

    lines_in_raw_data = raw_data.split('\n')

    data_in_each_line = []

    for line in lines_in_raw_data:
        splited = line.split(',')
        data_in_each_line.append(splited)

    index_line = data_in_each_line[0]
    del data_in_each_line[0]
    del data_in_each_line[-1]

    parsed_data_dict = {}

    for i in range(len(data_in_each_line)):

        for j in range(len(index_line)):
            to_be_key = index_line[j]
            to_be_value = data_in_each_line[i][j]
            try:
                parsed_data_dict[to_be_key].append(to_be_value)
            except:
                parsed_data_dict[to_be_key] = []
                parsed_data_dict[to_be_key].append(to_be_value)

    return parsed_data_dict

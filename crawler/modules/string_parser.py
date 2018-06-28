import json


def json_file_loader():
    json_data = {}

    with open('./desc.json', "r", encoding='utf-8') as json_file:
        json_data = json.load(json_file)

    one_line_string_list = _one_line_string_parser(json_data)
    word_list = _word_parser(one_line_string_list)

    dict = {
        "one_line_string_list": one_line_string_list,
        "word_list": word_list,
    }

    return dict


def _word_parser(one_line_string_list):
    word_list = []
    return_list = []

    for one_line_string in one_line_string_list:
        temp_word_list = one_line_string.split(' ')
        word_list.extend(temp_word_list)

        if len(word_list) > 110000:
            break

    for word in word_list:
        if (len(word) >= 2):
            return_list.append(word)

    return return_list


def _one_line_string_parser(json_data):
    one_line_string_list = []
    return_list = []

    for temp_dict in json_data['train']:
        temp_string = temp_dict['text']
        temp_string = temp_string.replace('\n\n\n', '\n')
        replaced_string = temp_string.replace('\n\n', '\n')
        temp_one_line_string_list = replaced_string.split('\n')
        one_line_string_list.extend(temp_one_line_string_list)

        if len(one_line_string_list) > 110000:
            break

    for i in range(len(one_line_string_list)):
        if one_line_string_list[i] != '':
            return_list.append(one_line_string_list[i])


    return return_list

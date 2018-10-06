import json


def json_file_loader():
    json_data = {}

    with open('/mnt/ssd512/goodday1478/json/desc.json', "r", encoding='utf-8') as json_file:
        json_data = json.load(json_file)

    one_line_string_list = _one_line_string_parser(json_data)
    word_list = _word_parser(one_line_string_list)

    dict = {
        "one_line_string_list": one_line_string_list,
        "word_list": word_list
    }

    return dict


def _word_parser(one_line_string_list):
    word_list = []
    return_list = []

    for one_line_string in one_line_string_list:
        temp_word_list = one_line_string.split(' ')
        word_list.extend(temp_word_list)

    for word in word_list:
        if (len(word) >= 5 and len(word) <= 7):
            return_list.append(word)

        if(len(return_list)== 500000):
            break
    print("word_parser_length", len(return_list))

    return return_list


def _one_line_string_parser(json_data):
    one_line_string_list = []
    return_list = []

    temp_list = json_data['train']

    for word in temp_list:
        temp_string = word["text"]
        temp_string = temp_string.replace('\n\n\n', '\n')
        replaced_string = temp_string.replace('\n\n', '\n')
        temp_one_line_string_list = replaced_string.split('\n')
        one_line_string_list.extend(temp_one_line_string_list)

        if len(one_line_string_list) > 500000:
            break

    for i in range(len(one_line_string_list)):
        if one_line_string_list[i] != '':
            return_list.append(one_line_string_list[i])

    print("length of line string parser", len(return_list))

    return return_list

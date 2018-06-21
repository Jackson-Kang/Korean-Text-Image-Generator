import random
import json


if __name__ == "__main__":

    print("\nShuffling...\n")

    data = {}

    with open('./data/generated_img_data/desc.json', encoding="utf-8") as json_file:
        data = json.load(json_file)

    random.shuffle(data["train"])
    random.shuffle(data["test"])

    with open('./data/generated_img_data/desc.json', 'w') as outfile:
        json.dump(data, outfile)

    print(data)

    print("\nComplete..!!\n")
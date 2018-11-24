import os
import json
import random


if __name__ == "__main__":

	file_dir_path = '/mnt/hdd640/goodday1478/json/'
	json_list = os.listdir(file_dir_path)

	json_data = {}

	output_json = {

		"train":[]
	}

	print("Start merging json files...")

	for i in range(len(json_list)):
		print("\t read "+ json_list[i] +" file...")
		with open(file_dir_path+json_list[i], 'r') as json_file:
			json_data = json.load(json_file)

		output_json["train"].extend(json_data["train"])
		random.shuffle(output_json["train"])
		# shuffle dataset

	print("\t\tfinished!")

	print("Start writing desc.json file...")

	with open(file_dir_path+'/desc.json', 'w', encoding='utf8') as json_file:
		json.dump(output_json, json_file, indent = 4, ensure_ascii= False)
	print("\tDone..!")


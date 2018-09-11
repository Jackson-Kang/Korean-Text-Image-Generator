import sys
import json
import random

from time import sleep

sys.path.append(sys.path[0] + '/modules/')

import crawler_module

def json_generate(temp_list):

	json_data = {
		"train":[],
		"test":[]
	}

	if count==repeat_numb:

		json_data["train"].extend(temp_list)
		with open("./desc.json", "a", encoding='utf-8') as json_file:
			json.dump(json_data, json_file, indent=4, ensure_ascii=False)


if __name__ == "__main__":

	repeat_numb = 200

	crawler = crawler_module.Crawler_Module()
	count = 0
	pass_count = 0
	user_input = input("search: ")
	temp_list = []

	while True:
		print("step: ", count, "th... generating...")
		crawler.set_user_input(user_input)
		try:
			result_list = crawler.crawler()
			user_input = crawler.find_less_crawled_element(result_list)	
		except:
			print("pass")
			pass_count += 1
			continue

		for string in result_list:
			string_dict = {"text": string}
			temp_list.append(string_dict)
		
		sleep(random.randrange(0, 10))

		if count==repeat_numb or pass_count==20:
			json_generate(temp_list)
			break

		count+=1

	print("\nFinish generating json!")

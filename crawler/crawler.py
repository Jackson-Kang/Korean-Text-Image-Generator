import sys
import json
import random

from time import sleep

sys.path.append(sys.path[0] + '/modules/')

import crawler_module

def json_generate(temp_list, repeat):

	json_data = {
		"train":[],
		"test":[]
	}

	if count==repeat_numb:

		json_data["train"].extend(temp_list)
		with open("/mnt/ssd512/goodday1478/json/desc"+str(repeat)+".json", "a", encoding='utf-8') as json_file:
			json.dump(json_data, json_file, indent=4, ensure_ascii=False)


if __name__ == "__main__":

	repeat_numb = 100

	crawler = crawler_module.Crawler_Module()
	count = 0
	repeat = 51
	pass_count = 0
	temp_list = []
	mode = "English"

	user_input = input("Search: ")

	while repeat <= 100:

		while True:
			print("\tStep: ", count, "th... generating...")
			crawler.set_user_input(user_input)
			try:
				result_list = crawler.crawler() 
				user_input = crawler.find_less_crawled_element(result_list, mode)	

			except Exception as ex:
				print("\t\tPass")
				print("\t\t\t Message:", ex)
				pass_count += 1

				if pass_count == 20:
					print("[Error] An error occured!")
					sys.exit()

				continue
	
			for string in result_list:
				string_dict = {"text": string}
				temp_list.append(string_dict)
		
			sleep(random.randrange(0, 10))
	
			if count==repeat_numb:
				json_generate(temp_list, repeat)
				break

			count+=1
		repeat += 1
		count = 0

	print("\nFinish generating json!")

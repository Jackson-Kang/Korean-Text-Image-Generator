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


	json_data["train"].extend(temp_list)

	with open("/mnt/hdd640/goodday1478/json/desc"+str(repeat)+".json", "a", encoding='utf-8') as json_file:
			json.dump(json_data, json_file, indent=4, ensure_ascii=False)


if __name__ == "__main__":


	crawler = crawler_module.Crawler_Module()
	count = 0
	repeat = 1
	max_repeat_numb = 300
	store_delimiter = 10
	pass_count = 0
	temp_list = []
	mode = "Korean"

	user_input = input("Search: ")

	while repeat <= max_repeat_numb:

		print("\n\tStep: ", repeat, "th... request...")
		while True:
			crawler.set_user_input(user_input)
			try:
				result_list = crawler.crawler() 
				user_input = crawler.find_less_crawled_element(result_list, mode)	

			except Exception as ex:
				print("\t\tPass")
				print("\t\t\t Message:", ex)
				pass_count += 1
				sleep(60)
				
				if pass_count == 3:
					print("[Error] An error occured!")
					sys.exit()

				continue
	
			for string in result_list:
				string_dict = {"text": string}
				temp_list.append(string_dict)
		
			sleep(random.randrange(0, 10))

			if count == store_delimiter:
				print("\t\t  done!")
				print("\t\tGenerating json files...")
				json_generate(temp_list, repeat)
				print("\t\t  done!")
				temp_list = []
				break

			count+=1
		repeat += 1
		count = 0

	print("\nFinish generating json!")

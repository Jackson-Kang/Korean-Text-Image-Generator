# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import urllib.request
import urllib.parse
import random
import re
from hanja import hangul


class Crawler_Module:

    user_input = ""

    def __init__(self):
        pass

    def crawler(self):
        default = 'https://openapi.naver.com/v1/search/news.xml?'
        sort = 'sort-sim'
        start = '&start=1'
        display = '&display=100'

        query = '&query=' + urllib.parse.quote_plus(self.user_input)
        fullURL = default + sort + start + display + query

        headers = {

            'Host': 'openapi.naver.com',
            'User-Agent': 'curl/7.43.0',
            'Accept': '*/*',
            'Content-Type': 'application/xml',
            'X-Naver-Client-Id': '83KxnTRcS8MkfM701ekt',
            'X-Naver-Client-Secret': 'Hifv0wG6Yu'
        }

        req = urllib.request.Request(fullURL, headers=headers)
        response = urllib.request.urlopen(req)
        # request to API Server

        status_code = response.getcode()

        if status_code == 200:

            result_XML = response.read()
            parsed_XML = BeautifulSoup(result_XML, 'lxml-xml')
            items = parsed_XML.find_all('item')

            result_list = []
            count = 1

            parse_chars = "[^가-힣0-9a-zA-Z\\s~`!@#$%^&*()-=_+ \\ |[\]{};':\",./<>?]"

            for item in items:
                title = self._strip_tag(item.title.get_text(strip=True))
                description = self._strip_tag(item.description.get_text(strip=True))

                temp_description = re.sub(parse_chars, '', description)

                if count%10 == 0:
                    temp_string = title + "\n" + temp_description
                else:
                    temp_string = title + "\n" + temp_description + "\n\n"

                result_list.append(temp_string)

            return result_list

        else:
            print("Crawler Error: " + str(status_code))
            return -1

    # issue -> convert chinese and korean into korean

    # return a parsed crawling results

    def _strip_tag(self, target_string):

        target_string = self._tag_converter(target_string, "&quot;", "\"")
        target_string = self._tag_converter(target_string, "<b>", "")
        target_string = self._tag_converter(target_string, "</b>", "")
        target_string = self._tag_converter(target_string, u'\xa0', ' ' )
        target_string = self._tag_converter(target_string, "&amp;", "&")
        target_string = self._tag_converter(target_string, "&lt;", "<")
        target_string = self._tag_converter(target_string, "&gt;", ">")
        target_string = self._tag_converter(target_string, "&nbsp;", " ")

        return target_string


    def _tag_converter(self, target_string, target_tag, converting_tag):
        # convert &quot; into " and erase <br> or </br>.
        temp_list = target_string.split(target_tag)
        result = converting_tag.join(temp_list)

        return result

    def set_user_input(self, user_input):
        self.user_input = user_input

    def find_less_crawled_element(self, string_list):

        min_element = []

        whole_string = self._tag_converter("".join(string_list), "\n\n", " ")
        whole_string = self._tag_converter(whole_string, "\n", " ")
        whole_string = self._tag_converter(whole_string, "/", "")
        temp_list = whole_string.split(" ")

        for word in temp_list:
            min_element.append((word, temp_list.count(word)))

        sorted_list = sorted(min_element, key = lambda key: key[1])

        min_list = []

        for tuple in sorted_list:
            if tuple[1] == 1:
                min_list.append(tuple[0])

        while True:
            return_val = random.choice(min_list)
            flag = 0
            for ch in return_val:
                if hangul.is_hangul(ch):
                    flag += 1
            if flag == len(return_val):
                break


        return return_val


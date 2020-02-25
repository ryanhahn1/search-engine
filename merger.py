from scanner import get_files, get_in_dir

import os
import json
import shutil as shu

def merge(file_1, file_2):
	word_total = 0
	with open(file_1, "r+", encoding='utf-8', errors='replace') as file1:
		with open(file_2, "r+", encoding='utf-8', errors='replace') as file2:
			iter1 = iter(file1)
			iter2 = iter(file2)
			output = ""
			line1 = next(iter1, None)
			line2 = next(iter2, None)
			while True:
				
				if line1 and line2:
					word1, list1str = line1.split(" ", 1)
					word2, list2str = line2.split(" ", 1)
					#print(word1, word2)
					list1 = json.loads(list1str.replace("\'", "\""))
					list2 = json.loads(list2str.replace("\'", "\""))
					#print(word2)
					#print(line1.split(" ", 1)[1])
					#list1 = json.loads(line1.split(" ", 1)[1])
					#list2 = json.loads(line2.split(" ", 1)[1])
					# merge these two lines and then add 
					if word1 == word2:
						listmerge = list1 + list2
						output += word1 + " " + json.dumps(listmerge) + "\n"
						line1 = next(iter1, None)
						line2 = next(iter2, None)
					# add word2
					elif word1 > word2:
						word_total += 1
						output += word2 + " " + json.dumps(list2) + "\n"
						line2 = next(iter2, None)
					# add word1
					else:
						word_total += 1
						output += word1 + " " + json.dumps(list1) + "\n"
						line1 = next(iter1, None)
				elif line1 == None and line2 == None:
					break
				elif line1 == None:
					output += line2
					line2 = next(iter2, None)
					word_total += 1
				elif line2 == None:
					output += line1
					line1 = next(iter1, None)
					word_total += 1
			file1.seek(0)
			file1.write(output)
			file1.truncate()
	print(get_word_count())


def multimerge(file_list):
	main_path = os.path.dirname(os.getcwd()) + "/index/main.txt"
	open(main_path, "w")
	shu.copyfile(file_list[0], main_path)
	current = 1
	while (current < len(file_list)):
		if ".DS_Store" not in file_list[current]:
			merge(main_path, file_list[current])
		current += 1

def get_word_count():
	with open(os.path.dirname(os.getcwd()) + "/index/main.txt") as main:
		count = 1
		for line in main:
			count += 1
	return count


if __name__ == '__main__':
	multimerge(get_files(os.path.dirname(os.getcwd()) + "/index/"))
	
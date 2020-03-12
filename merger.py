from scanner import get_files, get_in_dir

import os
import json
import shutil as shu

# compare 2 files and rewrite the first file with 
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
				# compare the current lines between both files
				if line1 and line2:
					word1, list1str = line1.split(" ", 1)
					word2, list2str = line2.split(" ", 1)
					list1 = json.loads(list1str)
					list2 = json.loads(list2str)
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
				# end of both files
				elif line1 == None and line2 == None:
					break
				# end of file 1, add the rest of file 2
				elif line1 == None:
					output += line2
					line2 = next(iter2, None)
					word_total += 1
				# end of file 2, add the rest of file 1
				elif line2 == None:
					output += line1
					line1 = next(iter1, None)
					word_total += 1
			# write the new document to the first file
			file1.seek(0)
			file1.write(output)
			file1.truncate()

# perform the merge operation on all batch files created during index
def multimerge(file_list):
	main_path = os.path.dirname(os.getcwd()) + "/index/not_main.txt"
	open(main_path, "w")
	shu.copyfile(file_list[0], main_path)
	current = 1
	while (current < len(file_list)):
		if ".txt" in file_list[current]:
			merge(main_path, file_list[current])
		current += 1

# scans the index and returns the number of tokens
def get_word_count():
	with open(os.path.dirname(os.getcwd()) + "/index/not_main.txt") as main:
		count = 1
		for line in main:
			count += 1
	return count


if __name__ == '__main__':
	multimerge(get_files(os.path.dirname(os.getcwd()) + "/index/"))
	
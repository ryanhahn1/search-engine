import json

def merge(file_1, file_2):
	with open(file_1, encoding='utf-8', errors='replace') as file1:
		with open(file_2, encoding='utf-8', errors='replace') as file2:
			iter1 = iter(file1)
			iter2 = iter(file2)
			output = ""
			line1 = next(iter1, None)
			line2 = next(iter2, None)
			while True:
				
				if line1 and line2:
					word1, list1str = line1.split(" ", 1)
					word2, list2str = line2.split(" ", 1)
					
					list1 = json.loads(list1str.replace("\'", "\""))
					list2 = json.loads(list2str.replace("\'", "\""))
					print(word1, word2)
					#print(word2)
					#print(line1.split(" ", 1)[1])
					#list1 = json.loads(line1.split(" ", 1)[1])
					#list2 = json.loads(line2.split(" ", 1)[1])
					# merge these two lines and then add 
					if word1 == word2:
						listmerge = list1 + list2
						output += word1 + " " + str(listmerge) + "\n"
						line1 = next(iter1, None)
						line2 = next(iter2, None)
					# add word2
					elif word1 > word2:
						output += word2 + " " + str(list2) + "\n"
						line2 = next(iter2, None)
					# add word1
					else:
						output += word1 + " " + str(list1) + "\n"
						line1 = next(iter1, None)
				elif line1 == None and line2 == None:
					print("REE break")
					break
				elif line1 == None:
					output += line2
					line2 = next(iter2, None)
				elif line2 == None:
					output += line1
					line1 = next(iter1, None)
			print(output)
			

path1 = "0.txt"
path2 = "1.txt"
merge(path1, path2)
file = open("configs.txt", "r")
file1 = open("/usr/src/linux/.config", "r")
some_list = []
for line in file:
	some_list.append(line.strip('\n') +"=")

print(some_list)
some_list2 = []
for line in file1:
	if any(substring in line for substring in some_list):
		some_list2.append(line)
print()
print(some_list2)
for substring in some_list:
	if not any(substring in string for string in some_list2):
		print(substring)

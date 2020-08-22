import re


def find_all_indexes(input_str, search_str):
    l1 = []
    length = len(input_str)
    index = 0
    while index < length:
        i = input_str.find(search_str, index)
        if i == -1:
            return l1
        l1.append(i)
        index = i + 1
    return l1

pattern = ". "
string = "This is the plan. This is going to work as per the schedule. This works!!!"

pos_map = {}

indices = find_all_indexes(string, pattern)

for m in indices:
    pos_map[m] = pattern

print(pos_map)
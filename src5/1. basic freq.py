import pickle
import re
import time
import sys

ENWIK_FILENAME = "../data/enwik9"
NUMBER_OF_LINES =  13147026
DISPLAY_CONTROL = 20000

COMBINING_FREQ_CHARS = 10000000


count = 0
nodes_dict = {}
with open(ENWIK_FILENAME, "r", encoding="utf-8") as f:
    print("The current approach is a little bit better so reading only one character at a time.")
    while True:
        letter = f.readline(1)
        count = count + 1
        if count % 1000000 == 0:
            print("------" + letter + "---" + str(count))
        if not letter:
            print("End of file")
            break
        if letter in nodes_dict:
            nodes_dict[letter] = nodes_dict[letter] + 1
        else:
            nodes_dict[letter] = 1



with open("../tmp/enwik8_total_usage_basic_chars", "w", encoding="utf-8", newline='\n') as f0:
    for k, v in sorted(nodes_dict.items(), key=lambda item: item[1], reverse=True):
        f0.write(k + "-" + str(v) + "\n")

final_map = {}
unfinal_map = {}

for k, v in sorted(nodes_dict.items(), key=lambda item: item[1], reverse=True):
    if v >= 100:
        final_map[k] = v

    else:
        unfinal_map[k] = v

with open("../tmp/important_chars", 'wb') as f:
    # Pickle the 'data' dictionary using the highest protocol available.
    pickle.dump(final_map, f, pickle.HIGHEST_PROTOCOL)

with open("../tmp/unimportant_chars", 'wb') as f:
    pickle.dump(unfinal_map, f, pickle.HIGHEST_PROTOCOL)

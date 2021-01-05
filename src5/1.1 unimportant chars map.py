import pickle
import re
import time
import sys
import math

ENWIK_FILENAME = "../data/enwik9"
NUMBER_OF_LINES =  13147026
DISPLAY_CONTROL = 20000

COMBINING_FREQ_CHARS = 10000000


unimportant_chars_map = {}
with open("../tmp/unimportant_chars", 'rb') as f:
    unimportant_chars_map = pickle.load(f)

length_of_code:int = math.ceil(math.log(len(unimportant_chars_map), 2))


final_unimportant_encoded_map = {}
index:int = 0
for k, v in sorted(unimportant_chars_map.items(), key=lambda item: {item[1], item[0]}, reverse=True):
    value:str = "{0:b}".format(index).zfill(length_of_code)
    print(value)
    final_unimportant_encoded_map[k] = value
    index = index + 1


with open("../tmp/unimportant_chars_encoded_map", 'wb') as f:
    pickle.dump(final_unimportant_encoded_map, f, pickle.HIGHEST_PROTOCOL)

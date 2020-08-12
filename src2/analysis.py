import io
import pickle
import re
import time

ENWIK_FILENAME = "../data/enwik9"
NUMBER_OF_LINES =  13147026
ENWIK_OUTPUT: str = "../tmp/enwik8_compressed"

first_word = None

start_time = time.time()


huffman_map_words = {}
with open("../tmp/enwik8_dict_words_huffman", 'rb') as f:
    huffman_map_words = pickle.load(f)

huffman_map = {}
with open("../tmp/enwik8_dict_huffman", 'rb') as f:
    huffman_map = pickle.load(f)

final_map = {}
with open("../tmp/enwik8_new_strucure_huffman_encoded", 'rb') as f:
    final_map = pickle.load(f)

count = 0
for key, value in final_map.items():
    if len(value) > 10000:
        count = count + 1
print(count)



print("Starting the analysis")
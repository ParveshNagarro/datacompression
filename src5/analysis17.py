import io
import time
import pickle
import re

#ENWIK_FILENAME = "../data/test.txt"
ENWIK_FILENAME = "../data/enwik9"
NUMBER_OF_LINES =  1314702
MIN_FREQ_TO_BE_A_WORD = 50


final_freq_map_combined_words = {}
with open("../tmp/enwik8_new_strucure_freq_distro_combined_words", 'rb') as f:
    final_freq_map_combined_words = pickle.load(f)


final_freq_map_words = {}
with open("../tmp/enwik8_new_strucure_freq_distro_words", 'rb') as f:
    final_freq_map_words = pickle.load(f)

final_freq_map = {}
with open("../tmp/enwik8_new_strucure_freq_distro", 'rb') as f:
    final_freq_map = pickle.load(f)

map  = {}
for k,v in final_freq_map_combined_words.items():
    freq = 0
    for k1,v1 in v.items():
        freq = freq + 1
    map[freq] = k

print("..")

with open("../tmp/freq_decider", "w", encoding="utf8") as f:
    for k, v in sorted(map.items(), key=lambda item: item[0], reverse=True):
        f.write(str(k) + "-" + v + "\n")


import io
import pickle
import re
import time

ENWIK_FILENAME = "../data/enwik9"
NUMBER_OF_LINES =  13147026
ENWIK_OUTPUT: str = "../tmp/enwik8_compressed"


final_map_combined_words = {}
with open("../tmp/enwik8_new_strucure_encoded_distro_combined_words", 'rb') as f:
    final_map_combined_words = pickle.load(f)


final_map_words = {}
with open("../tmp/enwik8_new_strucure_encoded_distro_words", 'rb') as f:
    final_map_words = pickle.load(f)

final_map = {}
with open("../tmp/enwik8_new_strucure_encoded_distro", 'rb') as f:
    final_map = pickle.load(f)




final_freq_map_combined_words = {}
with open("../tmp/enwik8_new_strucure_freq_distro_combined_words", 'rb') as f:
    final_freq_map_combined_words = pickle.load(f)


final_freq_map_words = {}
with open("../tmp/enwik8_new_strucure_freq_distro_words", 'rb') as f:
    final_freq_map_words = pickle.load(f)

final_freq_map = {}
with open("../tmp/enwik8_new_strucure_freq_distro", 'rb') as f:
    final_freq_map = pickle.load(f)

print(",,,")

total_usage = {}

for k, v in sorted(final_freq_map_combined_words.items(), key=lambda item: len(item[1]), reverse=True):
    total_usage[k] = len(v)

for k, v in sorted(final_freq_map_words.items(), key=lambda item: len(item[1]), reverse=True):
    total_usage[k] = len(v)

for k, v in sorted(final_freq_map.items(), key=lambda item: len(item[1]), reverse=True):
    total_usage[k] = len(v)


with open("../tmp1/enwik8_total_usage", "w", encoding="utf-8", newline='\n') as f0:
    for k, v in sorted(total_usage.items(), key=lambda item: item[1], reverse=True):
        f0.write(k + "-" + str(v) + "\n")

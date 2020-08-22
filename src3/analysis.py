import io
import pickle
import re
import time

ENWIK_FILENAME = "../data/enwik9"
NUMBER_OF_LINES =  13147026
ENWIK_OUTPUT: str = "../tmp/enwik8_compressed"

first_word = None

start_time = time.time()
MIN_FREQ_TO_BE_A_COMBINED_WORD = 1000
MIN_FREQ_TO_BE_A_WORD = 500

final_map_combined_words = {}
with open("../tmp/enwik8_new_strucure_freq_distro_combined_words", 'rb') as f:
    final_map_combined_words = pickle.load(f)



final_map_combined_words_old = {}
with open("../tmp - Copy/enwik8_new_strucure_huffman_encoded", 'rb') as f:
    final_map_combined_words_old = pickle.load(f)

keys_to_delete = {}
keys_to_add  = {}


print("Starting the analysis")
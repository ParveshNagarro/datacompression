import io
import time
import pickle
import re

#ENWIK_FILENAME = "../data/test.txt"
ENWIK_FILENAME = "../data/enwik9"
NUMBER_OF_LINES =  1314702
MIN_FREQ_TO_BE_A_WORD = 50




print("Here goes nothing!!!")
total_number_of_lines = NUMBER_OF_LINES
enwik: str = ENWIK_FILENAME
print("Reading the file " + enwik)


start_time = time.time()

count = 0
line_count = 0
print("creating the characters huffman tree now")

count = 0
nodes_dict = {}
with open(enwik, "r", encoding="utf-8") as f:
    print("The current approach is a little bit better so reading only one character at a time.")
    while True:
        letter = f.read(1)
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

print("total number of lines =  " + str(count))


print("This is the words array.. only putting the words with frequency greater than 1 in the dict")


with open("../tmp/a/enwik8_dict_huffman_orig", 'wb') as f:
    # Pickle the 'data' dictionary using the highest protocol available.
    pickle.dump(nodes_dict, f, pickle.HIGHEST_PROTOCOL)

print("--- %s seconds ---" % (time.time() - start_time))
total_len_orig = 0
with open("../tmp/a/enwik8_dict_huffman_text_orig", "w", encoding="utf-8", newline='\n') as f0:
    for k, v in sorted(nodes_dict.items(), key=lambda item: item[1], reverse=True):
        total_len_orig = total_len_orig + v
        f0.write(k + "-" + str(v) + "\n")

with open("../tmp/a/enwik8_total_orig", "w", encoding="utf-8", newline='\n') as f0:
        f0.write(str(total_len_orig))




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

nodes_dict = {}
total_len_orig = 0
for k, v in sorted(final_freq_map_combined_words.items(), key=lambda item: len(item[1]), reverse=True):
    freq = 0
    for k1, v1 in v.items():
        freq = freq + v1

    for letter in k:
        if letter in nodes_dict:
            nodes_dict[letter] = nodes_dict[letter] + freq
        else:
            nodes_dict[letter] = freq


for k, v in sorted(final_freq_map_words.items(), key=lambda item: len(item[1]), reverse=True):
    freq = 0
    for k1, v1 in v.items():
        freq = freq + v1

    for letter in k:
        if letter in nodes_dict:
            nodes_dict[letter] = nodes_dict[letter] + freq
        else:
            nodes_dict[letter] = freq

for k, v in sorted(final_freq_map.items(), key=lambda item: len(item[1]), reverse=True):
    freq = 0
    for k1, v1 in v.items():
        freq = freq + v1

    letter = k
    if letter in nodes_dict:
        nodes_dict[letter] = nodes_dict[letter] + freq
    else:
        nodes_dict[letter] = freq

total_len_orig = 0
with open("../tmp/a/enwik8_dict_huffman_text_maps", "w", encoding="utf-8", newline='\n') as f0:
    for k, v in sorted(nodes_dict.items(), key=lambda item: item[1], reverse=True):
        total_len_orig = total_len_orig + v
        f0.write(k + "-" + str(v) + "\n")


with open("../tmp/a/enwik8_total_maps", "w", encoding="utf-8", newline='\n') as f0:
        f0.write(str(total_len_orig))

with open("../tmp/a/enwik8_dict_huffman_maps", 'wb') as f:
    # Pickle the 'data' dictionary using the highest protocol available.
    pickle.dump(nodes_dict, f, pickle.HIGHEST_PROTOCOL)

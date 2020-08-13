import pickle
import re
import time
import sys

ENWIK_FILENAME = "../data/enwik9"
NUMBER_OF_LINES =  13147026
MIN_FREQ_TO_BE_A_WORD = 2


# Back up the reference to the exceptionhook
sys._excepthook = sys.excepthook

def my_exception_hook(exctype, value, traceback):
    # Print the error and traceback
    print(exctype, value, traceback)
    # Call the normal Exception hook after
    sys._excepthook(exctype, value, traceback)
    sys.exit(1)

# Set the exception hook to our wrapping function
sys.excepthook = my_exception_hook

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


start_time = time.time()

huffman_map_words = {}
with open("../tmp/enwik8_dict_words_huffman", 'rb') as f:
    huffman_map_words = pickle.load(f)

huffman_map = {}
with open("../tmp/enwik8_dict_huffman", 'rb') as f:
    huffman_map = pickle.load(f)

encoded_contents = ""
print("Reading the dicts is complete, now creating the new structure.")

cutoff = 0

enwik: str = ENWIK_FILENAME
count = 100000000

final_map = {}

newCount = 0
current_word = None
with open(enwik, "r", encoding="utf-8") as f:
    while True:
        c = f.readline()
        if newCount % 200000 == 0:
            print("--- %s seconds ---" % (time.time() - start_time))
            print("Compressing - " + str((newCount * 100) / NUMBER_OF_LINES))
        newCount = newCount + 1
        if not c:
            print("End of file. writing whatever is left")
            break

        line_words_pos_dict = {}

        for key, value in huffman_map_words.items():
            indices = find_all_indexes(c, key)

            for m in indices:
                line_words_pos_dict[m] = key

        iter_index = 0
        while iter_index < len(c):
            new_word = None
            if iter_index in line_words_pos_dict.keys():
                new_word = line_words_pos_dict[iter_index]
                iter_index = iter_index + len(line_words_pos_dict[iter_index])
            else:
                new_word = c[iter_index]
                iter_index = iter_index + 1

            if current_word is None:
                current_word = new_word
                final_map[new_word] = {}
            else:
                if new_word not in final_map:
                    final_map[new_word] = {}
                if new_word not in final_map[current_word]:
                    final_map[current_word][new_word] = 1
                else:
                    final_map[current_word][new_word] = final_map[current_word][new_word] + 1
                current_word = new_word


with open("../tmp/enwik8_new_strucure_freq_distro", 'wb') as f:
    # Pickle the 'data' dictionary using the highest protocol available.
    pickle.dump(final_map, f, pickle.HIGHEST_PROTOCOL)

huffman_map = {}
huffman_map_words = {}
for key, value in final_map.items():
    if len(key) > 1:
        total_freq = 0
        for k,v in value.items():
            total_freq = total_freq + v
        if total_freq >= MIN_FREQ_TO_BE_A_WORD:
            huffman_map_words[key] = 1
        else:
            for character_t in k:
                huffman_map[character_t] = 1
    else:
        huffman_map[key] = 1

    for k,v in value.items():
        if v >= MIN_FREQ_TO_BE_A_WORD:
            huffman_map_words[key + k] = 1

with open("../tmp/enwik8_dict_huffman", 'wb') as f:
    # Pickle the 'data' dictionary using the highest protocol available.
    pickle.dump(huffman_map, f, pickle.HIGHEST_PROTOCOL)



with open("../tmp/enwik8_dict_words_huffman", 'wb') as f:
    # Pickle the 'data' dictionary using the highest protocol available.
    pickle.dump(huffman_map_words, f, pickle.HIGHEST_PROTOCOL)


print("--- %s seconds ---" % (time.time() - start_time))
import io
import pickle
import re
import time

ENWIK_FILENAME = "../data/enwik9"
NUMBER_OF_LINES =  13147026
ENWIK_OUTPUT: str = "../tmp/enwik8_compressed"

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

encoded_contents = ""

print("Reading the dicts is complete, it's time to write the file back.")

print("The compressed version will be written to " + ENWIK_OUTPUT)
cutoff = 0

first_word = None
current_word = None


newCount = 0
total_number_of_lines = NUMBER_OF_LINES
print("doing the compression")
with open(ENWIK_OUTPUT, "w+b") as fo:
    with open(ENWIK_FILENAME, "r", encoding="utf-8") as f:
        while True:
            c = f.readline()
            if newCount % 10000 == 0:
                print("Compressing - " + str((newCount * 100) / total_number_of_lines))
                print("--- %s seconds ---" % (time.time() - start_time))
            newCount = newCount + 1
            if not c:
                print("End of file. writing whatever is left")
                bytes_array = []
                while len(encoded_contents) > 0:
                    if len(encoded_contents) > 8:
                        string_to_write = encoded_contents[:8]
                        encoded_contents = encoded_contents[8:]
                        bytes_array.append(int(string_to_write, 2))
                    else:
                        string_to_write = encoded_contents
                        encoded_contents = ""
                        cutoff = 8 - len(string_to_write)
                        bytes_array.append(int(string_to_write, 2))
                        string_to_write = encoded_contents + ("0" * cutoff)

                fo.write(bytearray(bytes_array))

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

                if first_word is None:
                    first_word = new_word
                    current_word = first_word
                else:
                    if (len(final_map[current_word])) > 1:
                        encoded_contents = encoded_contents + final_map[current_word][new_word]

                    current_word = new_word


            while len(encoded_contents) > 8:
                bytes_array = []
                string_to_write = encoded_contents[:8]
                encoded_contents = encoded_contents[8:]
                bytes_array.append(int(string_to_write, 2))
                fo.write(bytearray(bytes_array))

print("cutoff" + str(cutoff))
with open("../tmp/enwik8_cutoff", 'wb') as f:
    # Pickle the 'data' dictionary using the highest protocol available.
    pickle.dump(cutoff, f, pickle.HIGHEST_PROTOCOL)

print("--- %s seconds ---" % (time.time() - start_time))

with open("../tmp/enwik8_first_word", 'wb') as f:
    # Pickle the 'data' dictionary using the highest protocol available.
    pickle.dump(first_word, f, pickle.HIGHEST_PROTOCOL)

print("--- %s seconds ---" % (time.time() - start_time))
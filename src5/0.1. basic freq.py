import pickle
import re
import time
import sys

ENWIK_FILENAME = "../data/enwik9"
NUMBER_OF_LINES =  13147026
DISPLAY_CONTROL = 20000

COMBINING_FREQ_CHARS = 10000000


count = 0
words_freq_dict = {}
line_count = 0
with open(ENWIK_FILENAME, "r", encoding="utf-8") as f:
    print("Creating a list of words... .")
    while True:
        line = f.readline()
        count = count + 1
        line_count = line_count + 1
        if line_count % 10000 == 0:
            print("Creating the words dict - " + str(line_count))
        if not line:
            print("End of file")
            break

        words = re.findall(r'\w+', line)

        for word in words:
            if len(word) > 1:
                if word in words_freq_dict:
                    words_freq_dict[word] = words_freq_dict[word] + 1
                else:
                    words_freq_dict[word] = 1

print("total number of lines =  " + str(count))

with open("../tmp/words_enwik8_total_usage_basic_chars", "w", encoding="utf-8", newline='\n') as f0:
    for k, v in sorted(words_freq_dict.items(), key=lambda item: item[1], reverse=True):
        f0.write(k + "-" + str(v) + "\n")


words_final_map = {}

for k, v in sorted(words_freq_dict.items(), key=lambda item: item[1], reverse=True):
    if v >= 10000:
        words_final_map[k] = v

with open("../tmp/words_important_chars", 'wb') as f:
    # Pickle the 'data' dictionary using the highest protocol available.
    pickle.dump(words_final_map, f, pickle.HIGHEST_PROTOCOL)


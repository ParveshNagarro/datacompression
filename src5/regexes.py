import  pickle

MIN_FREQ_TO_BE_A_COMBINED_WORD = 100

final_map_words = {}
with open("../tmp/enwik8_new_strucure_freq_distro_words", 'rb') as f:
    final_map_words = pickle.load(f)


combined_words = {}

for key, value in final_map_words.items():
    for k,v in value.items():
        if v >= MIN_FREQ_TO_BE_A_COMBINED_WORD:
            combined_words[key + k] = {}

with open("../tmp/enwik8_new_strucure_freq_distro_combined_words", 'wb') as f:
    # Pickle the 'data' dictionary using the highest protocol available.
    pickle.dump(combined_words, f, pickle.HIGHEST_PROTOCOL)

import pickle

COMBINING_FREQ_CHARS = 1000000

final_map = {}
with open("../tmp/enwik8_new_strucure_freq_distro", 'rb') as f:
    final_map = pickle.load(f)

final_map_1 = {}
for key, value in sorted(final_map.items(), key=lambda item: len(item[1]), reverse=True):
    for k, v in value.items():
        if v >= COMBINING_FREQ_CHARS:
            final_map_1[key + k] = v

with open("../tmp/enwik8_words_new_strucure_freq_distro", 'wb') as f:
    pickle.dump(final_map_1, f, pickle.HIGHEST_PROTOCOL)
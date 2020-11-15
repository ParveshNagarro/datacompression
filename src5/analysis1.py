import io
import time
import pickle
import re

#ENWIK_FILENAME = "../data/test.txt"
ENWIK_FILENAME_CHARACTERS = "../tmp/analysis/enwik8_new_strucure_freq_distro"
ENWIK_FILENAME_WORDS = "../tmp/analysis/enwik8_new_strucure_freq_distro_words"
ENWIK_FILENAME_COMBINED_WORDS = "../tmp/analysis/enwik8_new_strucure_freq_distro_combined_words"
NUMBER_OF_LINES =  1314702
MIN_FREQ_TO_BE_A_WORD = 50



class Node:
    character: str
    encoded_string: str
    frequency: int
    children: []

    def __init__(self, character: str, frequency: int):
        self.character = character
        self.frequency = frequency
        self.children = []
        self.encoded_string = ""


print("!!! Reading the files !!!")

print("!!! Reading the combined words file !!!")
final_map_combined_words = {}
with open(ENWIK_FILENAME_COMBINED_WORDS, 'rb') as f:
    final_map_combined_words = pickle.load(f)

print("Number of combined words in combined words map : " + str(len(final_map_combined_words)))


print("!!! Writing the keys from the combined words file !!!")
with open("../tmp/analysis/keys/combined_words.txt", "w", encoding="utf-8", newline='\n') as f0:
    for key, value in final_map_combined_words.items():
        total_freq = 0
        for k, v in value.items():
            total_freq = total_freq + v
        f0.write("\"" + key + "\"" + "-" + str(total_freq) + "\n")



print("!!! Reading the words file !!!")
final_map_words = {}
with open(ENWIK_FILENAME_WORDS, 'rb') as f:
    final_map_words = pickle.load(f)

print("Number of words in words map : " + str(len(final_map_words)))

print("!!! Writing the keys from the words file !!!")
with open("../tmp/analysis/keys/words.txt", "w", encoding="utf-8", newline='\n') as f0:
    for key, value in final_map_words.items():
        total_freq = 0
        for k, v in value.items():
            total_freq = total_freq + v
        f0.write("\"" + key + "\"" + "-" + str(total_freq) + "\n")


print("!!! Reading the characters file !!!")
final_map = {}
with open(ENWIK_FILENAME_CHARACTERS, 'rb') as f:
    final_map = pickle.load(f)

print("Number of characters in characters map : " + str(len(final_map)))

print("!!! Writing the keys from the characters file !!!")
with open("../tmp/analysis/keys/characters.txt", "w", encoding="utf-8", newline='\n') as f0:
    for key, value in final_map.items():
        total_freq = 0
        for k, v in value.items():
            total_freq = total_freq + v
        f0.write("\"" + key + "\"" + "-" + str(total_freq) + "\n")
import io
import pickle
import re

class Node:
    character: str
    frequency: int
    children: []
    final_children_dict: {}

    def __init__(self, character: str, frequency: int):
        self.character = character
        self.frequency = frequency
        self.children = []
        self.final_children_dict = {}

# the program starts here

print("Here goes nothing!!!")
total_number_of_lines = 1128024
enwik: str = "../../data/tmp/enwik81.txt"
print("Reading the file " + enwik)

word_nodes_dict = {}
line_count = 0
with open(enwik, "r", encoding="utf-8") as f:
    print("Creating a list of words... .")
    while True:
        line = f.readline()
        line_count = line_count + 1
        if line_count % 10000 == 0:
            print("Creating the words dict - " + str((line_count * 100) / total_number_of_lines))
        if not line:
            print("End of file")
            break

        words = re.findall(r'\w+', line)

        for word in words:
            if len(word) > 1:
                if word in word_nodes_dict:
                    node: Node = word_nodes_dict[word]
                    node.frequency = node.frequency + 1
                else:
                    node = Node(word, 1)
                    word_nodes_dict[word] = node

print("total number of lines =  " + str(line_count))


print("This is the words array.. only putting the words with frequency greater than 1 in the dict")
final_word_nodes_dict = {}
for key, value in word_nodes_dict.items():
    if value.frequency >= 1000:
        final_word_nodes_dict[key] = value

with open("../../data/tmp/enwik8_dict_words", 'wb') as f:
    pickle.dump(final_word_nodes_dict, f, pickle.HIGHEST_PROTOCOL)

count = 0
nodes_dict = {}
with open(enwik, "r", encoding="utf-8") as f:
    print("The current approach is a little bit better so reading only one character at a time.")
    while True:
        letter = f.readline(1)
        count = count + 1
        if count % 1000000 == 0:
            print("------" + letter + "---" + str(count))
        if not letter:
            print("End of file")
            break
        if letter in nodes_dict:
            node: Node = nodes_dict[letter]
            node.frequency = node.frequency + 1
        else:
            node = Node(letter, 1)
            nodes_dict[letter] = node

print("total number of lines =  " + str(count))

print("Subtracting the frequencies that are being used by the words  ")
for key, value in final_word_nodes_dict.items():
    word_string:str = key
    word_freq:int = value.frequency
    for letter_part_of_word in word_string:
        nodes_dict[letter_part_of_word].frequency = nodes_dict[letter_part_of_word].frequency - word_freq


print("This is the words array.. only putting the words with frequency greater than 1 in the dict")
final_nodes_dict = {}
for key, value in nodes_dict.items():
    if value.frequency > 0:
        final_nodes_dict[key] = value


with open("../../data/tmp/enwik8_dict_chars", 'wb') as f:
    pickle.dump(final_nodes_dict, f, pickle.HIGHEST_PROTOCOL)



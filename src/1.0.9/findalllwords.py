import io
import pickle
import re

class Node:
    character: str
    frequency: int
    children: []
    final_children_dict: {}
    children_rare: []
    final_children_dict_rare: {}
    is_rare_children_node:bool

    def __init__(self, character: str, frequency: int):
        self.character = character
        self.frequency = frequency
        self.children = []
        self.encoded_string = ""
        self.final_children_dict = {}
        self.final_children_dict_rare: {}
        self.is_rare_children_node = False

# the program starts here

print("Here goes nothing!!!")
total_number_of_lines = 1128024
enwik: str = "../../data/tmp/enwik8"
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

words_list = []
for key, value in word_nodes_dict.items():
    words_list.append(value)



words_list.sort(key=lambda x: x.frequency, reverse=True)

print("This is the words array.. only putting the words with frequency greater than 1 in the dict")
with open("../../data/tmp/analysis/allwords.txt", "w", encoding="utf-8", newline='\n') as f:
    for value in words_list:
        f.write(value.character + "    " + str(value.frequency) + "\n")

import io
import pickle
import re

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


def huffman_iteration(huffman_tree_to_iterate):
    print("Sorting the nodes in the tree. Right now there are " + str(len(huffman_tree_to_iterate)) + " nodes.")
    huffman_tree_to_iterate.sort(key=lambda x: x.frequency, reverse=False)
    node1 = huffman_tree_to_iterate.pop(0)
    node2 = huffman_tree_to_iterate.pop(0)
    print("Creating a new node with characters " + node1.character + node2.character + "  and string " + str(
        node1.frequency + node2.frequency))
    new_node = Node(node1.character + node2.character, node1.frequency + node2.frequency)
    new_node.children.append(node1)
    new_node.children.append(node2)
    huffman_tree_to_iterate.append(new_node)
    print("Sorting the nodes in the tree. Right now there are " + str(len(huffman_tree_to_iterate)) + " nodes.")
    huffman_tree_to_iterate.sort(key=lambda x: x.frequency, reverse=False)


def encode_the_node(node):
    print("The current node to encode is " + str(node.frequency) + "-" + node.character)
    if node.children is not None and 0 < len(node.children):
        print("Encoding the node " + str(node.frequency) + "-" + node.character)
        print("Now encoding the first child of the node + " + str(node.frequency) + "-" + node.character)
        node.children[0].encoded_string = node.encoded_string + "0"
        encode_the_node(node.children[0])
        if len(node.children) > 1:
            print("Now encoding the second child of the node + " + str(node.frequency) + "-" + node.character)
            node.children[1].encoded_string = node.encoded_string + "1"
            encode_the_node(node.children[1])
    else:
        print("Nothing to encode in this node as there are either no children")


def print_a_node(node):
    string_to_print = str(node.frequency) + "-" + node.character + "-" + node.encoded_string
    if node.children is not None and 0 < len(node.children):
        string_to_print += "-> \n\t"
        string_to_print += print_a_node(node.children[0]) + " , "
        if len(node.children) > 1:
            string_to_print += print_a_node(node.children[1])
    return string_to_print


def print_a_list(nodes_list_to_print):
    print("printing a list")
    for node_to_print in nodes_list_to_print:
        print(print_a_node(node_to_print))


# the program starts here

print("Here goes nothing!!!")
total_number_of_lines = 1128024
enwik: str = "../../data/tmp/enwik8"
print("Reading the file " + enwik)

count = 0
word_nodes_dict = {}
line_count = 0
with open(enwik, "r", encoding="utf-8") as f:
    print("Creating a list of words... .")
    while True:
        line = f.readline()
        count = count + 1
        line_count = line_count + 1
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

print("total number of lines =  " + str(count))


print("This is the words array.. only putting the words with frequency greater than 1 in the dict")
final_word_nodes_dict = {}
for key, value in word_nodes_dict.items():
    if value.frequency >= 500:
        final_word_nodes_dict[key] = value

print("Converting the final dict into a list of nodes")
word_nodes_list = []
for key, value in final_word_nodes_dict.items():
    word_nodes_list.append(value)

word_nodes_list.sort(key=lambda x: x.frequency, reverse=False)

print("The entire contents after the sorting and node creations")
print_a_list(word_nodes_list)

word_huffman_tree = []
for value in word_nodes_list:
    word_huffman_tree.append(value)

print("Iterating and merging the nodes until only one remains")
while len(word_huffman_tree) > 1:
    huffman_iteration(word_huffman_tree)
print_a_list(word_huffman_tree)

encode_the_node(word_huffman_tree[0])
print_a_list(word_huffman_tree)

with open("../../data/tmp/enwik8_dict_words", 'wb') as f:
    # Pickle the 'data' dictionary using the highest protocol available.
    pickle.dump(word_huffman_tree, f, pickle.HIGHEST_PROTOCOL)

print("creating the characters huffman tree now")

count = 0
nodes_dict = {}
with open(enwik, "r", encoding="utf-8") as f:
    print("The current approach is a little bit better so reading only one character at a time.")
    while True:
        letter = f.readline(1)
        count = count + 1
        if count % 10000 == 0:
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

print("Converting the dict into a list of nodes")
nodes_list = []
for key, value in final_nodes_dict.items():
    nodes_list.append(value)
nodes_list.sort(key=lambda x: x.frequency, reverse=False)

print("The entire contents after the sorting and node creations")
print_a_list(nodes_list)

huffman_tree = []
for value in nodes_list:
    huffman_tree.append(value)

print("Iterating and merging the nodes until only one remains")
while len(huffman_tree) > 1:
    huffman_iteration(huffman_tree)
print_a_list(huffman_tree)

encode_the_node(huffman_tree[0])
print_a_list(huffman_tree)

with open("../../data/tmp/enwik8_dict_chars", 'wb') as f:
    # Pickle the 'data' dictionary using the highest protocol available.
    pickle.dump(huffman_tree, f, pickle.HIGHEST_PROTOCOL)




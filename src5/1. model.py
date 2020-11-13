import io
import time
import pickle
import re

#ENWIK_FILENAME = "../data/test.txt"
ENWIK_FILENAME = "../data/enwik9"
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


def convert_freq_map_to_huffman_map(final_word_nodes_dict, fileName) :
    print("Converting the final dict into a list of nodes")

    word_nodes_list = []
    for key, value in final_word_nodes_dict.items():
        new_node = Node(key, value)
        word_nodes_list.append(new_node)

    word_nodes_list.sort(key=lambda x: x.frequency, reverse=False)

    tmp_words_nodes_list = []
    for word in word_nodes_list:
        tmp_words_nodes_list.append(word)

    tmp_words_nodes_list.sort(key=lambda x: x.frequency, reverse=True)

    with open(fileName, "w", encoding="utf8") as f:
        for node_tmp_1 in tmp_words_nodes_list:
            f.write(node_tmp_1.character + " - " + str(node_tmp_1.frequency) + "\n")

    word_huffman_tree = []
    for value in word_nodes_list:
        word_huffman_tree.append(value)

    print("Iterating and merging the nodes until only one remains")
    while len(word_huffman_tree) > 1:
        huffman_iteration(word_huffman_tree)

    encode_the_node(word_huffman_tree[0])

    result = {}
    for node_tmp in tmp_words_nodes_list:
        result[node_tmp.character] = node_tmp.encoded_string

    return result


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
total_number_of_lines = NUMBER_OF_LINES
enwik: str = ENWIK_FILENAME
print("Reading the file " + enwik)


start_time = time.time()

count = 0
words_freq_dict = {}
line_count = 0
with open(enwik, "r", encoding="utf-8") as f:
    print("Creating a list of words... .")
    while True:
        line = f.readline()
        count = count + 1
        line_count = line_count + 1
        if line_count % 10000 == 0:
            print("Creating the words dict - " + str((line_count * 100) / total_number_of_lines))
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


print("This is the words array.. only putting the words with frequency greater than 1 in the dict")
final_words_freq_dict = {}
for key, value in words_freq_dict.items():
    if value >= MIN_FREQ_TO_BE_A_WORD:
        final_words_freq_dict[key] = value

huffman_map_words = convert_freq_map_to_huffman_map(final_words_freq_dict, "../tmp/frequency_distro_words")

with open("../tmp/enwik8_dict_words_huffman", 'wb') as f:
    # Pickle the 'data' dictionary using the highest protocol available.
    pickle.dump(huffman_map_words, f, pickle.HIGHEST_PROTOCOL)
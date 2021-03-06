import pickle
import re
import time
import sys
import datetime
import concurrent
import concurrent.futures

ENWIK_FILENAME = "../data/enwik9"
NUMBER_OF_LINES =  13147026
MIN_FREQ_TO_BE_A_WORD = 500
MIN_FREQ_TO_BE_A_COMBINED_WORD = 1000
DISPLAY_CONTROL = 20000

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

class TrieNode:
    character:str
    children:{}
    is_terminal:bool

    def __init__(self, character: str, is_terminal: bool):
        self.character = character
        self.is_terminal = is_terminal
        self.children = {}


def create_trie_for_huffman_map(huffman_map):
    root:TrieNode = TrieNode("root", False)
    for key, value in huffman_map.items():
        current_trie_node:TrieNode = root
        for char_key in key:
            if char_key in current_trie_node.children:
                current_trie_node = current_trie_node.children[char_key]
            else:
                new_trie_node = TrieNode(char_key, False)
                current_trie_node.children[char_key] = new_trie_node
                current_trie_node = new_trie_node
        current_trie_node.is_terminal = True
    return root



def convert_freq_map_to_huffman_map(final_word_nodes_dict) :
    print("Converting the final dict into a list of nodes" + str(len(final_word_nodes_dict)))

    word_nodes_list = []
    for key, value in final_word_nodes_dict.items():
        new_node = Node(key, value)
        word_nodes_list.append(new_node)

    word_huffman_tree = []
    for value in word_nodes_list:
        word_huffman_tree.append(value)

    #print("Iterating and merging the nodes until only one remains")
    if len(word_huffman_tree) > 1:
        iter_count = 0
        while len(word_huffman_tree) > 1:
            iter_count = iter_count + 1
            if iter_count % 1000 == 0:
                print(" current number of nodes " + str(len(word_huffman_tree)))
            huffman_iteration(word_huffman_tree)
    else:
        if len(word_huffman_tree) == 1:
            node1 = word_huffman_tree.pop(0)
            root_node = Node("root", 1)
            root_node.children.append(node1)
            word_huffman_tree.append(root_node)

    encode_the_node(word_huffman_tree[0])

    result = {}
    for node_tmp in word_nodes_list:
        result[node_tmp.character] = node_tmp.encoded_string

    return result


def huffman_iteration(huffman_tree_to_iterate):
    #print("Sorting the nodes in the tree. Right now there are " + str(len(huffman_tree_to_iterate)) + " nodes.")
    huffman_tree_to_iterate.sort(key=lambda x: x.frequency, reverse=False)
    node1 = huffman_tree_to_iterate.pop(0)
    node2 = huffman_tree_to_iterate.pop(0)

    ##print("Creating a new node with characters " + node1.character + node2.character + "  and string " + str(
      #  node1.frequency + node2.frequency))
    new_node = Node(node1.character + node2.character, node1.frequency + node2.frequency)
    new_node.children.append(node1)
    new_node.children.append(node2)
    huffman_tree_to_iterate.append(new_node)



def encode_the_node(node):
    #print("The current node to encode is " + str(node.frequency) + "-" + node.character)
    if node.children is not None and 0 < len(node.children):
#        print("Encoding the node " + str(node.frequency) + "-" + node.character)
#        print("Now encoding the first child of the node + " + str(node.frequency) + "-" + node.character)
        node.children[0].encoded_string = node.encoded_string + "0"
        encode_the_node(node.children[0])
        if len(node.children) > 1:
#            print("Now encoding the second child of the node + " + str(node.frequency) + "-" + node.character)
            node.children[1].encoded_string = node.encoded_string + "1"
            encode_the_node(node.children[1])
#    else:
#        print("Nothing to encode in this node as there are either no children")


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


def convert_key_val_to_huffman_map(map, key, value,name):
    if len(value) > 0:
        map[key] = convert_freq_map_to_huffman_map(value)
    print(name + " Current map size --- " + str(len(map)))

start_time = time.time()



final_map_combined_words = {}
with open("../tmp/analysis/enwik8_new_strucure_freq_distro_combined_words", 'rb') as f:
    final_map_combined_words = pickle.load(f)

final_map_combined_words_1 = {}
first_kay = None
first_value = None

count= 0
for key, value in sorted(final_map_combined_words.items(), key=lambda item: len(item[1]), reverse=True):
    if count == 100:
        first_kay = key
        first_value = value
        break
    count = count + 1



with open("../tmp/analysis/enwik8_total_usage.txt", "w", encoding="utf-8", newline='\n') as f0:
    f0.write(first_kay + "\n")
    for k, v in sorted(first_value.items(), key=lambda item: item[1], reverse=True):
        f0.write(k + "-" + str(v) + "\n")


print("--- %s seconds ---" % (time.time() - start_time))
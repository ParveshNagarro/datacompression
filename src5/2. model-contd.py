import pickle
import re
import time
import sys

ENWIK_FILENAME = "../data/enwik9"
NUMBER_OF_LINES =  13147026
DISPLAY_CONTROL = 20000
UNIMPORTANT_CHARS = "專"

COMBINING_FREQ_CHARS = 10000000

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

def convert_freq_map_to_huffman_map(final_word_nodes_dict, fileName="tmp") :
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
    if len(word_huffman_tree) > 1:
        while len(word_huffman_tree) > 1:
            huffman_iteration(word_huffman_tree)
    else:
        if len(word_huffman_tree) == 1:
            node1 = word_huffman_tree.pop(0)
            root_node = Node("root", 1)
            root_node.children.append(node1)
            word_huffman_tree.append(root_node)

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


def get_new_char(character_read, important_characters_map):
    new_char = character_read
    if new_char not in important_characters_map:
        new_char = UNIMPORTANT_CHARS
    return new_char


start_time = time.time()


important_chars_map = {}
with open("../tmp/important_chars", 'rb') as f:
    important_chars_map = pickle.load(f)

final_map = {}

count = 0
current_word = None
total_count = 0
with open(ENWIK_FILENAME, "r", encoding="utf-8") as f:
    while True:
        c = f.readline()
        if count % DISPLAY_CONTROL == 0:
            print("--- %s seconds ---" % (time.time() - start_time))
            print("Compressing - " + str((count * 100) / NUMBER_OF_LINES))
        count = count + 1
        if not c:
            print("End of file. writing whatever is left")
            break

        # iterating over the trie repeatedly
        iter_index = 0
        while iter_index < len(c):
            total_count = total_count + 1
            new_word = get_new_char(c[iter_index], important_chars_map)
            iter_index = iter_index + 1

            if current_word is None:
                total_count = total_count + 1
                new_word = new_word + get_new_char(c[iter_index], important_chars_map)
                iter_index = iter_index + 1

                total_count = total_count + 1
                new_word = new_word + get_new_char(c[iter_index], important_chars_map)
                iter_index = iter_index + 1

                current_word = new_word
                if new_word not in final_map:
                    final_map[new_word] = {}
            else:

                key_to_use = current_word[1:] + new_word
                if key_to_use not in final_map:
                    final_map[key_to_use] = {}

                if new_word not in final_map[current_word]:
                    final_map[current_word][new_word] = 1
                else:
                    final_map[current_word][new_word] = final_map[current_word][new_word] + 1
                current_word = key_to_use


new_word = "<<<----EOF---------------EOF---------------->>>"
final_map[current_word][new_word]=1

with open("../tmp/enwik8_new_strucure_freq_distro", 'wb') as f:
    pickle.dump(final_map, f, pickle.HIGHEST_PROTOCOL)
print("--- %s seconds ---" % (time.time() - start_time))

print("total count  " + str(total_count))
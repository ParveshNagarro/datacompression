import pickle
import re
import time
import sys

ENWIK_FILENAME = "../data/enwik9"
NUMBER_OF_LINES =  13147026


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


start_time = time.time()

huffman_map_words = {}
with open("../tmp/enwik8_dict_words_huffman", 'rb') as f:
    huffman_map_words = pickle.load(f)

huffman_map = {}
with open("../tmp/enwik8_dict_huffman", 'rb') as f:
    huffman_map = pickle.load(f)

encoded_contents = ""

print("Reading the dicts is complete, now creating the new structure.")

cutoff = 0

enwik: str = ENWIK_FILENAME
count = 100000000

final_map = {}

newCount = 0
current_word = None
with open(enwik, "r", encoding="utf-8") as f:
    while True:
        c = f.readline()
        if newCount % 200000 == 0:
            print("--- %s seconds ---" % (time.time() - start_time))
            print("Compressing - " + str((newCount * 100) / NUMBER_OF_LINES))
        newCount = newCount + 1
        if not c:
            print("End of file. writing whatever is left")

            break

        line_all_words = {}
        words_in_line = re.findall(r'\w+', c)
        for word in words_in_line:
            if word in huffman_map_words:
                line_all_words[word] = huffman_map_words[word]

        line_words_pos_dict = {}
        for key, value in line_all_words.items():
            cursor = 0
            index:int = c.find(key, cursor)
            while index != -1:
                if index in line_words_pos_dict.keys():
                    if len(line_words_pos_dict[index]) < len(key):
                        line_words_pos_dict[index] = key
                else:
                    line_words_pos_dict[index] = key
                cursor = cursor + len(key)
                index: int = c.find(key, cursor)

        iter_index = 0
        while iter_index < len(c):
            new_word = None
            if iter_index in line_words_pos_dict.keys():
                new_word = line_words_pos_dict[iter_index]
                iter_index = iter_index + len(line_words_pos_dict[iter_index])
            else:
                new_word = c[iter_index]
                iter_index = iter_index + 1

            if current_word is None:
                current_word = new_word
                final_map[new_word] = {}
            else:
                if new_word not in final_map:
                    final_map[new_word] = {}
                if new_word not in final_map[current_word]:
                    final_map[current_word][new_word] = 1
                else:
                    final_map[current_word][new_word] = final_map[current_word][new_word] + 1
                current_word = new_word

final_huffman_map = {}
for key,value in final_map.items():
    if len(value) > 0:
        final_map[key] = convert_freq_map_to_huffman_map(value)

with open("../tmp/enwik8_new_strucure_freq_distro", 'wb') as f:
    # Pickle the 'data' dictionary using the highest protocol available.
    pickle.dump(final_map, f, pickle.HIGHEST_PROTOCOL)

with open("../tmp/enwik8_new_strucure_huffman_encoded", 'wb') as f:
    # Pickle the 'data' dictionary using the highest protocol available.
    pickle.dump(final_map, f, pickle.HIGHEST_PROTOCOL)


print("--- %s seconds ---" % (time.time() - start_time))
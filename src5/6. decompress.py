import io
import time
import pickle
import sys
import concurrent
import concurrent.futures

ENWIK_FILENAME = "../data/enwik9"
NUMBER_OF_LINES =  13147026
TOTAL_COUNT = 469800763

start_time = time.time()

class Node:
    character: str
    encoded_string: str
    frequency: int
    children: []
    character_huff: ""

    def __init__(self, character: str, frequency: int):
        self.character = character
        self.frequency = frequency
        self.children = []
        self.encoded_string = ""
        self.character_huff = ""


# Back up the reference to the exceptionhook
sys._excepthook = sys.excepthook

def my_exception_hook(exctype, value, traceback):
    # Print the  r and traceback
    print(exctype, value, traceback)
    # Call the normal Exception hook after
    sys._excepthook(exctype, value, traceback)
    sys.exit(1)

# Set the exception hook to our wrapping function
sys.excepthook = my_exception_hook



def convert_freq_map_to_huffman_map(final_word_nodes_dict, current_word) :
    print("Converting the final dict into a list of nodes ---------------" + current_word + "---------" + str(len(final_word_nodes_dict)))

    word_nodes_list = []
    for key, value in final_word_nodes_dict.items():
        new_node = Node(key, value)
        word_nodes_list.append(new_node)

    word_nodes_list.sort(key=lambda x: (x.frequency, x.character), reverse=False)

    tmp_words_nodes_list = []
    for word in word_nodes_list:
        tmp_words_nodes_list.append(word)

    tmp_words_nodes_list.sort(key=lambda x: (x.frequency, x.character), reverse=True)

    word_huffman_tree = []
    for value in word_nodes_list:
        word_huffman_tree.append(value)

    #print("Iterating and merging the nodes until only one remains")
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
    #print("Sorting the nodes in the tree. Right now there are " + str(len(huffman_tree_to_iterate)) + " nodes.")
    huffman_tree_to_iterate.sort(key=lambda x: (x.frequency, x.character), reverse=False)
    node1 = huffman_tree_to_iterate.pop(0)
    node2 = huffman_tree_to_iterate.pop(0)
    #print("Creating a new node with characters " + node1.character + node2.character + "  and string " + str(
   #     node1.frequency + node2.frequency))
    new_node = Node(node1.character + node2.character, node1.frequency + node2.frequency)
    new_node.children.append(node1)
    new_node.children.append(node2)
    huffman_tree_to_iterate.append(new_node)
   # print("Sorting the nodes in the tree. Right now there are " + str(len(huffman_tree_to_iterate)) + " nodes.")
    huffman_tree_to_iterate.sort(key=lambda x: (x.frequency, x.character), reverse=False)


def encode_the_node(node):
    #print("The current node to encode is " + str(node.frequency) + "-" + node.character)
    if node.children is not None and 0 < len(node.children):
        #print("Encoding the node " + str(node.frequency) + "-" + node.character)
    #    print("Now encoding the first child of the node + " + str(node.frequency) + "-" + node.character)
        node.children[0].encoded_string = node.encoded_string + "0"
        encode_the_node(node.children[0])
        if len(node.children) > 1:
        #    print("Now encoding the second child of the node + " + str(node.frequency) + "-" + node.character)
            node.children[1].encoded_string = node.encoded_string + "1"
            encode_the_node(node.children[1])
 #   else:
    #    print("Nothing to encode in this node as there are either no children")


def print_a_node(node):
    string_to_print = str(node.frequency) + "-" + node.character + "-" + node.encoded_string
    if node.children is not None and 0 < len(node.children):
        string_to_print += "-> \n\t"
        string_to_print += print_a_node(node.children[0]) + " , "
        if len(node.children) > 1:
            string_to_print += print_a_node(node.children[1])
    return string_to_print


def print_a_list(nodes_list_to_print):
  #  print("printing a list")
    for node_to_print in nodes_list_to_print:
        print(print_a_node(node_to_print))


def encode_the_node(node):
    #print("The current node to encode is " + str(node.frequency) + "-" + node.character)
    if node.children is not None and 0 < len(node.children):
        #print("Encoding the node " + str(node.frequency) + "-" + node.character)
        #print("Now encoding the first child of the node + " + str(node.frequency) + "-" + node.character)
        node.children[0].encoded_string = node.encoded_string + "0"
        encode_the_node(node.children[0])
        if len(node.children) > 1:
           # print("Now encoding the second child of the node + " + str(node.frequency) + "-" + node.character)
            node.children[1].encoded_string = node.encoded_string + "1"
            encode_the_node(node.children[1])
    #else:
     #   print("Nothing to encode in this node as there are either no children")


def convert_huffman_map_to_tree(huffman_map_input):
    result_huffman_tree = []
    root = Node("root", 1)
    result_huffman_tree.append(root)

    for key, value in huffman_map_input.items():
        current_node = root
        for character_huff in value[:-1]:

            child_node_found = None
            for child_node_to_check in current_node.children:
                if child_node_to_check.character_huff == character_huff:
                    child_node_found = child_node_to_check

            if child_node_found is not None:
                current_node = child_node_found
            else:
                tmp_node = Node(character_huff, 1)
                tmp_node.character_huff = character_huff
                if character_huff == "1":
                    current_node.children.insert(1, tmp_node)
                else:
                    current_node.children.insert(0, tmp_node)
                current_node = tmp_node

        new_node = Node(key, 1)
        new_node.encoded_string = value
        new_node.character_huff = value[-1]
        if value[-1] == "1":
            current_node.children.insert(1, new_node)
        else:
            current_node.children.insert(0, new_node)

    return result_huffman_tree


def convert_key_value_final_map_to_tree(huffman_map_input, key, value, string_to_print, name):
    print(string_to_print + key)
    huffman_map_input[key] = convert_huffman_map_to_tree(value)[0]
    print(name + " Current map size --- " + str(len(huffman_map_input)))





final_map = {}
with open("../tmp/enwik8_new_strucure_encoded_distro", 'rb') as f:
    final_map = pickle.load(f)

final_map_1 = {}
for key,value in sorted(final_map.items(), key=lambda item: len(item[1]), reverse=True):
    convert_key_value_final_map_to_tree(final_map_1, key, value,
                                        "3.converting the final map to sub tree of the items", "characters map")
print("writing third one")
with open("../tmp/enwik8_new_strucure_encoded_distro_1", 'wb') as f:
    # Pickle the 'data' dictionary using the highest protocol available.
    pickle.dump(final_map_1, f, pickle.HIGHEST_PROTOCOL)




final_map_words = {}
with open("../tmp/enwik8_words_new_strucure_encoded_distro", 'rb') as f:
    final_map_words = pickle.load(f)

final_map_words_1 = {}
for key,value in sorted(final_map_words.items(), key=lambda item: len(item[1]), reverse=True):
    convert_key_value_final_map_to_tree(final_map_words_1, key, value,
                                        "3.converting the final map to sub tree of the items", "characters map")

print("writing third one")
with open("../tmp/enwik8_words_new_strucure_encoded_distro_1", 'wb') as f:
    pickle.dump(final_map_words_1, f, pickle.HIGHEST_PROTOCOL)


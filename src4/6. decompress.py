import io
import time
import pickle
import sys

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

    word_nodes_list.sort(key=lambda x: x.frequency, reverse=False)

    tmp_words_nodes_list = []
    for word in word_nodes_list:
        tmp_words_nodes_list.append(word)

    tmp_words_nodes_list.sort(key=lambda x: x.frequency, reverse=True)

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


final_map_combined_words = {}
with open("../tmp/enwik8_new_strucure_encoded_distro_combined_words", 'rb') as f:
    final_map_combined_words = pickle.load(f)

final_map_words = {}
with open("../tmp/enwik8_new_strucure_encoded_distro_words", 'rb') as f:
    final_map_words = pickle.load(f)

final_map = {}
with open("../tmp/enwik8_new_strucure_encoded_distro", 'rb') as f:
    final_map = pickle.load(f)



final_frequency_map_combined_words = {}
with open("../tmp/enwik8_new_strucure_freq_distro_combined_words", 'rb') as f:
    final_frequency_map_combined_words = pickle.load(f)

final_frequency_map_words = {}
with open("../tmp/enwik8_new_strucure_freq_distro_words", 'rb') as f:
    final_frequency_map_words = pickle.load(f)

final_frequency_map = {}
with open("../tmp/enwik8_new_strucure_freq_distro", 'rb') as f:
    final_frequency_map = pickle.load(f)



for key,value in final_map_combined_words.items():
    print("converting the final map to sub tree of the items")
    final_map_combined_words[key] = convert_huffman_map_to_tree(value)[0]

for key,value in final_map_words.items():
    print("converting the final map to sub tree of the items")
    final_map_words[key] = convert_huffman_map_to_tree(value)[0]


for key,value in final_map.items():
    print("converting the final map to sub tree of the items")
    final_map[key] = convert_huffman_map_to_tree(value)[0]


cutoff_in = 0
cutoff = 0
with open("../tmp/enwik8_cutoff", 'rb') as f:
    cutoff_in = pickle.load(f)


first_word = ""
with open("../tmp/enwik8_first_word", 'rb') as f:
    first_word = pickle.load(f)

map_containing_keys_to_delete = {}

current_word = first_word
output_final = first_word
current_node = None
decoded_string = ""

newCount = 0

debugCount = 0
with open("../tmp/enwik8_output", "w", encoding="utf-8", newline='\n') as f0:
    with open("../tmp/enwik8_compressed", "rb") as f:
        byte = f.read(1)
        while byte != b"":
            # Do stuff with byte.
            newCount = newCount + 1
            if newCount % 100000 == 0:
                print("percentage of file read" + str((newCount * 100) / TOTAL_COUNT))

            byte_temp = byte
            byte = f.read(1)
            decoded_string = "{0:b}".format(ord(byte_temp))

            cutoff = 8 - len(decoded_string)
            if byte == b"":
                cutoff = cutoff - cutoff_in
                if cutoff < 0:
                    cutoff = 0

            decoded_string = ("0" * cutoff) + decoded_string

            tmp_decoding_string = decoded_string


            for character in tmp_decoding_string:

                if current_node is None:

                    map_to_use = final_map
                    if len(current_word) > 1:
                        if current_word in final_map_combined_words:
                            map_to_use = final_map_combined_words
                        else:
                            map_to_use = final_map_words

                    current_node = map_to_use[current_word]

                while len(current_node.children) == 1:
                    current_node = current_node.children[0]
                    output_final = output_final + current_node.character

                    freq_map_to_use = final_frequency_map
                    map_to_use = final_map
                    if len(current_word) > 1:
                        if current_word in final_map_combined_words:
                            freq_map_to_use =  final_frequency_map_combined_words
                            map_to_use = final_map_combined_words
                        else:
                            freq_map_to_use = final_frequency_map_words
                            map_to_use = final_map_words

                    freq_map_to_use[current_word][current_node.character] = freq_map_to_use[current_word][current_node.character] - 1
                    if freq_map_to_use[current_word][current_node.character] == 0:
                        del map_to_use[current_word][current_node.character]
                        del freq_map_to_use[current_word][current_node.character]

                        if len(freq_map_to_use[current_word]) > 0:
                            if len(freq_map_to_use[current_word]) < 10:
                                map_to_use[current_word] = convert_huffman_map_to_tree(convert_freq_map_to_huffman_map(freq_map_to_use[current_word], current_word))
                            else:
                                if current_word in map_containing_keys_to_delete:
                                    map_containing_keys_to_delete[current_word] = map_containing_keys_to_delete[current_word] + 1
                                else:
                                    map_containing_keys_to_delete[current_word] = 1

                                if map_containing_keys_to_delete[current_word] >= 20:
                                    del map_containing_keys_to_delete[current_word]
                                    map_to_use[current_word] = convert_huffman_map_to_tree(convert_freq_map_to_huffman_map(freq_map_to_use[current_word], current_word))

                        else:
                            del map_to_use[current_word]
                            del freq_map_to_use[current_word]
                            print("fun fun fun fun-----" + str(len(map_to_use)))


                    current_word = current_node.character

                    map_to_use = final_map
                    if len(current_word) > 1:
                        if current_word in final_map_combined_words:
                            map_to_use = final_map_combined_words
                        else:
                            map_to_use = final_map_words

                    current_node = map_to_use[current_word]

                if character == "1":
                    current_node = current_node.children[1]
                else:
                    current_node = current_node.children[0]


                if len(current_node.children) == 0:
                    output_final = output_final + current_node.character

                    freq_map_to_use = final_frequency_map
                    map_to_use = final_map
                    if len(current_word) > 1:
                        if current_word in final_map_combined_words:
                            freq_map_to_use =  final_frequency_map_combined_words
                            map_to_use = final_map_combined_words
                        else:
                            freq_map_to_use = final_frequency_map_words
                            map_to_use = final_map_words

                    freq_map_to_use[current_word][current_node.character] = freq_map_to_use[current_word][current_node.character] - 1
                    if freq_map_to_use[current_word][current_node.character] == 0:
                        del map_to_use[current_word][current_node.character]
                        del freq_map_to_use[current_word][current_node.character]

                        if len(freq_map_to_use[current_word]) > 0:
                            if len(freq_map_to_use[current_word]) < 10:
                                map_to_use[current_word] = convert_huffman_map_to_tree(convert_freq_map_to_huffman_map(freq_map_to_use[current_word], current_word))
                            else:
                                if current_word in map_containing_keys_to_delete:
                                    map_containing_keys_to_delete[current_word] = map_containing_keys_to_delete[current_word] + 1
                                else:
                                    map_containing_keys_to_delete[current_word] = 1

                                if map_containing_keys_to_delete[current_word] >= 20:
                                    del map_containing_keys_to_delete[current_word]
                                    map_to_use[current_word] = convert_huffman_map_to_tree(convert_freq_map_to_huffman_map(freq_map_to_use[current_word], current_word))

                        else:
                            del map_to_use[current_word]
                            del freq_map_to_use[current_word]
                            print("fun fun fun fun-----" + str(len(map_to_use)))


                    current_word = current_node.character
                    current_node = None

                    # here keep updating directly if there is only one child

                    if len(output_final) > 8:
                        tmp_output_final = output_final[:8]
                        output_final = output_final[8:]
                        f0.write(tmp_output_final)

        if len(output_final) > 0:
            f0.write(output_final)

print("--- %s seconds ---" % (time.time() - start_time))


with open("../tmp2/enwik8_new_strucure_freq_distro", 'wb') as f:
    # Pickle the 'data' dictionary using the highest protocol available.
    pickle.dump(final_frequency_map, f, pickle.HIGHEST_PROTOCOL)

with open("../tmp2/enwik8_new_strucure_freq_distro_words", 'wb') as f:
    # Pickle the 'data' dictionary using the highest protocol available.
    pickle.dump(final_frequency_map_words, f, pickle.HIGHEST_PROTOCOL)

with open("../tmp2/enwik8_new_strucure_freq_distro_combined_words", 'wb') as f:
    # Pickle the 'data' dictionary using the highest protocol available.
    pickle.dump(final_frequency_map_combined_words, f, pickle.HIGHEST_PROTOCOL)
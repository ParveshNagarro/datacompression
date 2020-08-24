import io
import pickle
import re
import time
import sys

ENWIK_FILENAME = "../data/enwik9"
NUMBER_OF_LINES =  13147026
ENWIK_OUTPUT: str = "../tmp/enwik8_compressed"
DISPLAY_CONTROL = 2000


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


def convert_freq_map_to_huffman_map(final_word_nodes_dict,current_word) :
    print("Converting the final dict into a list of nodes------" +  current_word + "-------" + str(len(final_word_nodes_dict)))

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
    huffman_tree_to_iterate.sort(key=lambda x: x.frequency, reverse=False)
    node1 = huffman_tree_to_iterate.pop(0)
    node2 = huffman_tree_to_iterate.pop(0)
    #print("Creating a new node with characters " + node1.character + node2.character + "  and string " + str(
        #node1.frequency + node2.frequency))
    new_node = Node(node1.character + node2.character, node1.frequency + node2.frequency)
    new_node.children.append(node1)
    new_node.children.append(node2)
    huffman_tree_to_iterate.append(new_node)
    #print("Sorting the nodes in the tree. Right now there are " + str(len(huffman_tree_to_iterate)) + " nodes.")
    huffman_tree_to_iterate.sort(key=lambda x: x.frequency, reverse=False)


def encode_the_node(node):
    #print("The current node to encode is " + str(node.frequency) + "-" + node.character)
    if node.children is not None and 0 < len(node.children):
        #print("Encoding the node " + str(node.frequency) + "-" + node.character)
        #print("Now encoding the first child of the node + " + str(node.frequency) + "-" + node.character)
        node.children[0].encoded_string = node.encoded_string + "0"
        encode_the_node(node.children[0])
        if len(node.children) > 1:
            #print("Now encoding the second child of the node + " + str(node.frequency) + "-" + node.character)
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


first_word = None

start_time = time.time()


final_map_combined_words = {}
with open("../tmp/enwik8_new_strucure_encoded_distro_combined_words", 'rb') as f:
    final_map_combined_words = pickle.load(f)

combined_words_helper = {}

for key, value in final_map_combined_words.items():
    words_in_line = re.findall(r'\w+', key)
    for word in words_in_line:
        if word in combined_words_helper:
            combined_words_helper[word].append(key)
        else:
            combined_words_helper[word] = [key]


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

encoded_contents = ""

print("Reading the dicts is complete, it's time to write the file back.")

print("The compressed version will be written to " + ENWIK_OUTPUT)
cutoff = 0

first_word = None
current_word = None

map_containing_keys_to_delete = {}

newCount = 0
total_number_of_lines = NUMBER_OF_LINES
print("doing the compression")
with open(ENWIK_OUTPUT, "w+b") as fo:
    with open(ENWIK_FILENAME, "r", encoding="utf-8") as f:
        while True:
            c = f.readline()
            if newCount % DISPLAY_CONTROL == 0:
                print("Compressing - " + str((newCount * 100) / total_number_of_lines))
                print("--- %s seconds ---" % (time.time() - start_time))
            newCount = newCount + 1
            if not c:
                print("End of file. writing whatever is left")
                bytes_array = []
                while len(encoded_contents) > 0:
                    if len(encoded_contents) > 8:
                        string_to_write = encoded_contents[:8]
                        encoded_contents = encoded_contents[8:]
                        bytes_array.append(int(string_to_write, 2))
                    else:
                        string_to_write = encoded_contents
                        encoded_contents = ""
                        cutoff = 8 - len(string_to_write)
                        bytes_array.append(int(string_to_write, 2))
                        string_to_write = encoded_contents + ("0" * cutoff)

                fo.write(bytearray(bytes_array))

                break
            line_all_words = {}
            words_in_line = re.findall(r'\w+', c)
            for word in words_in_line:
                if word in final_map_words:
                    line_all_words[word] = final_map_words[word]

            line_words_pos_dict = {}
            for key, value in line_all_words.items():
                cursor = 0
                index: int = c.find(key, cursor)
                while index != -1:
                    if index in line_words_pos_dict:
                        if len(line_words_pos_dict[index]) < len(key):
                            line_words_pos_dict[index] = key
                    else:
                        line_words_pos_dict[index] = key
                    cursor = cursor + len(key)
                    index: int = c.find(key, cursor)

            combined_words_helper_client = {}
            for word in words_in_line:
                if word in combined_words_helper:
                    list_of_combined_word = combined_words_helper[word]
                    for combined_word in list_of_combined_word:
                        if combined_word in final_map_combined_words:
                            combined_words_helper_client[combined_word] = final_map_combined_words[combined_word]

            for key, value in combined_words_helper_client.items():
                cursor = 0
                index: int = c.find(key, cursor)
                while index != -1:
                    if index in line_words_pos_dict:
                        if len(line_words_pos_dict[index]) < len(key):
                            line_words_pos_dict[index] = key
                    else:
                        line_words_pos_dict[index] = key
                    cursor = cursor + len(key)
                    index: int = c.find(key, cursor)


            iter_index = 0
            while iter_index < len(c):
                new_word = None
                if iter_index in line_words_pos_dict:
                    new_word = line_words_pos_dict[iter_index]
                    iter_index = iter_index + len(line_words_pos_dict[iter_index])
                else:
                    new_word = c[iter_index]
                    iter_index = iter_index + 1

                if first_word is None:
                    first_word = new_word
                    current_word = first_word
                else:

                    map_to_use = final_map
                    freq_map_to_use = final_frequency_map
                    if len(current_word) > 1:
                        if current_word in final_map_combined_words:
                            map_to_use = final_map_combined_words
                            freq_map_to_use = final_frequency_map_combined_words
                        else:
                            map_to_use = final_map_words
                            freq_map_to_use = final_frequency_map_words

                    if (len(map_to_use[current_word])) > 1:
                        encoded_contents = encoded_contents + map_to_use[current_word][new_word]

                    freq_map_to_use[current_word][new_word] = freq_map_to_use[current_word][new_word] - 1

                    if freq_map_to_use[current_word][new_word] == 0:
                        del map_to_use[current_word][new_word]
                        del freq_map_to_use[current_word][new_word]

                        if len(freq_map_to_use[current_word]) > 0:
                            if len(freq_map_to_use[current_word]) < 10:
                                map_to_use[current_word] = convert_freq_map_to_huffman_map(freq_map_to_use[current_word], current_word)
                            else:
                                if current_word in map_containing_keys_to_delete:
                                    map_containing_keys_to_delete[current_word] = map_containing_keys_to_delete[current_word] + 1
                                else:
                                    map_containing_keys_to_delete[current_word] = 1

                                if map_containing_keys_to_delete[current_word] >= 20:
                                    del map_containing_keys_to_delete[current_word]
                                    map_to_use[current_word] = convert_freq_map_to_huffman_map(freq_map_to_use[current_word], current_word)
                        else:
                            del map_to_use[current_word]
                            del freq_map_to_use[current_word]
                            print("fun fun fun fun-----" + str(len(map_to_use)))

                    current_word = new_word


            while len(encoded_contents) > 8:
                bytes_array = []
                string_to_write = encoded_contents[:8]
                encoded_contents = encoded_contents[8:]
                bytes_array.append(int(string_to_write, 2))
                fo.write(bytearray(bytes_array))

print("cutoff" + str(cutoff))
with open("../tmp/enwik8_cutoff", 'wb') as f:
    # Pickle the 'data' dictionary using the highest protocol available.
    pickle.dump(cutoff, f, pickle.HIGHEST_PROTOCOL)

print("--- %s seconds ---" % (time.time() - start_time))

with open("../tmp/enwik8_first_word", 'wb') as f:
    # Pickle the 'data' dictionary using the highest protocol available.
    pickle.dump(first_word, f, pickle.HIGHEST_PROTOCOL)

print("--- %s seconds ---" % (time.time() - start_time))


with open("../tmp1/enwik8_new_strucure_freq_distro", 'wb') as f:
    # Pickle the 'data' dictionary using the highest protocol available.
    pickle.dump(final_frequency_map, f, pickle.HIGHEST_PROTOCOL)

with open("../tmp1/enwik8_new_strucure_freq_distro_words", 'wb') as f:
    # Pickle the 'data' dictionary using the highest protocol available.
    pickle.dump(final_frequency_map_words, f, pickle.HIGHEST_PROTOCOL)

with open("../tmp1/enwik8_new_strucure_freq_distro_combined_words", 'wb') as f:
    # Pickle the 'data' dictionary using the highest protocol available.
    pickle.dump(final_frequency_map_combined_words, f, pickle.HIGHEST_PROTOCOL)
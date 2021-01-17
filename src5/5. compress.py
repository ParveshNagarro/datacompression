import pickle
import time
import sys

ENWIK_FILENAME = "../data/enwik9"
NUMBER_OF_LINES =  13147026
ENWIK_OUTPUT: str = "../tmp/enwik8_compressed"
DISPLAY_CONTROL = 4000


UNIMPORTANT_CHARS = "專"

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

  
def convert_freq_map_to_huffman_map(final_word_nodes_dict,current_word) :
    #print("Converting the final dict into a list of nodes------" +  current_word + "-------" + str(len(final_word_nodes_dict)))

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
        #node1.frequency + node2.frequency))
    new_node = Node(node1.character + node2.character, node1.frequency + node2.frequency)
    new_node.children.append(node1)
    new_node.children.append(node2)
    huffman_tree_to_iterate.append(new_node)
    #print("Sorting the nodes in the tree. Right now there are " + str(len(huffman_tree_to_iterate)) + " nodes.")
    huffman_tree_to_iterate.sort(key=lambda x: (x.frequency, x.character), reverse=False)


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



def populate_total_usage(a, b, total_usage_map):

    map_to_use = total_usage_map

    key = "\"" + a + "-" + b + "\""

    if key in map_to_use:
        map_to_use[key] = map_to_use[key] + 1
    else:
        map_to_use[key] = 1


def get_new_char(character_read, important_characters_map):
    new_char = character_read
    if new_char not in important_characters_map:
        new_char = UNIMPORTANT_CHARS
    return new_char


first_word = None

start_time = time.time()


final_map = {}
with open("../tmp/enwik8_new_strucure_encoded_distro", 'rb') as f:
    final_map = pickle.load(f)



final_frequency_map = {}
with open("../tmp/enwik8_new_strucure_freq_distro", 'rb') as f:
    final_frequency_map = pickle.load(f)


important_chars_map = {}
with open("../tmp/important_chars", 'rb') as f:
    important_chars_map = pickle.load(f)


unimportant_chars_encoded_map = {}
with open("../tmp/unimportant_chars_encoded_map", 'rb') as f:
    unimportant_chars_encoded_map = pickle.load(f)


encoded_contents = ""

total_usage = {}

print("Reading the dicts is complete, it's time to write the file back.")

print("The compressed version will be written to " + ENWIK_OUTPUT)
cutoff = 0



first_word = None
current_word = None


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

            if newCount == 450:
                print("debug dbeug debug")

            iter_index = 0
            while iter_index < len(c):
                terminal_node_index = None


                # this will the be the second value in the substring operator[iter_index:end_iter_index]
                end_iter_index = iter_index
                # did not find anything, just using single length string i.e. a character.
                if terminal_node_index is None:
                    end_iter_index = end_iter_index + 1
                else:
                    end_iter_index = terminal_node_index

                tmp_new_word = c[iter_index:end_iter_index]
                new_word = tmp_new_word
                if len(new_word) == 1:
                    new_word = get_new_char(new_word, important_chars_map)
                iter_index = iter_index + len(new_word)


                if first_word is None:
                    tmp_new_word = c[iter_index]
                    new_word = new_word + get_new_char(tmp_new_word, important_chars_map)
                    iter_index = iter_index + 1

                    tmp_new_word = c[iter_index]
                    new_word = new_word + get_new_char(tmp_new_word, important_chars_map)
                    iter_index = iter_index + 1

                    first_word = new_word
                    current_word = first_word
                else:

                    map_to_use = final_map
                    freq_map_to_use = final_frequency_map

                    if (len(map_to_use[current_word])) > 1:
                        if new_word == UNIMPORTANT_CHARS:
                            encoded_contents = encoded_contents + map_to_use[current_word][new_word] + unimportant_chars_encoded_map[tmp_new_word]
                            populate_total_usage(current_word, new_word, total_usage)
                        else:
                            encoded_contents = encoded_contents + map_to_use[current_word][new_word]
                            populate_total_usage(current_word, new_word, total_usage)
                    elif new_word == UNIMPORTANT_CHARS:
                        encoded_contents = encoded_contents + unimportant_chars_encoded_map[tmp_new_word]
                        populate_total_usage(current_word, new_word, total_usage)




                    if current_word == '\n= ' and new_word == '&':
                        print("a")
                    freq_map_to_use[current_word][new_word] = freq_map_to_use[current_word][new_word] - 1

                    if freq_map_to_use[current_word][new_word] == 0:
                        del map_to_use[current_word][new_word]
                        del freq_map_to_use[current_word][new_word]

                        if len(freq_map_to_use[current_word]) > 0:
                            if len(freq_map_to_use[current_word]) <= 10:
                                map_to_use[current_word] = convert_freq_map_to_huffman_map(freq_map_to_use[current_word], current_word)
                        else:
                            del map_to_use[current_word]
                            del freq_map_to_use[current_word]
                            print("fun fun fun fun-----" + str(len(map_to_use)))

                    key_to_use = current_word[1:] + new_word
                    current_word = key_to_use

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


with open("../tmp/enwik8_total_usage", "w", encoding="utf-8", newline='\n') as f0:
    for k, v in sorted(total_usage.items(), key=lambda item: item[1], reverse=True):
        f0.write(k + "-" + str(v) + "\n")


import io
import pickle
import re
import time

#ENWIK_FILENAME = "../data/test.txt"
ENWIK_FILENAME = "../data/enwik9"
NUMBER_OF_LINES =  13147026

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


def append_the_node(huffman_tree_node: Node, nodes_collect:{}):
    if len(huffman_tree_node.children) > 0:
        append_the_node(huffman_tree_node.children[0], nodes_collect)
        if (len(huffman_tree_node.children)) > 1:
            append_the_node(huffman_tree_node.children[1], nodes_collect)
    else:
        nodes_collect[huffman_tree_node.character] = huffman_tree_node


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
                if child_node_to_check.character == character_huff:
                    child_node_found = child_node_to_check

            if child_node_found is not None:
                current_node = child_node_found
            else:
                tmp_node = Node(character_huff, 1)
                if character_huff == "1":
                    current_node.children.insert(1, tmp_node)
                else:
                    current_node.children.insert(0, tmp_node)
                current_node = tmp_node

        new_node = Node(key, 1)
        new_node.encoded_string = value
        if value[-1] == "1":
            current_node.children.insert(1, new_node)
        else:
            current_node.children.insert(0, new_node)

    return result_huffman_tree


start_time = time.time()

huffman_map_words = {}
with open("../tmp/enwik8_dict_words_huffman", 'rb') as f:
    huffman_map_words = pickle.load(f)

huffman_map = {}
with open("../tmp/enwik8_dict_huffman", 'rb') as f:
    huffman_map = pickle.load(f)

huffman_tree_chars = convert_huffman_map_to_tree(huffman_map)
huffman_tree_words = convert_huffman_map_to_tree(huffman_map_words)

huffman_tree = []

root_node:Node = Node("root", 0)
root_node.children.append(huffman_tree_chars[0])
root_node.children.append(huffman_tree_words[0])

huffman_tree.append(root_node)

encode_the_node(huffman_tree[0])

nodes_dict_words = {}
append_the_node(huffman_tree_words[0], nodes_dict_words)

nodes_dict_chars = {}
append_the_node(huffman_tree_chars[0], nodes_dict_chars)

encoded_contents = ""

print("Reading the dicts is complete, it's time to write the file back.")
enwik_output: str = "../tmp/enwik8_compressed"
print("The compressed version will be written to " + enwik_output)
cutoff = 0

enwik: str = ENWIK_FILENAME
count = 100000000

newCount = 0
total_number_of_lines = NUMBER_OF_LINES
print("doing the compression")
with open(enwik_output, "w+b") as fo:
    with open(enwik, "r", encoding="utf-8") as f:
        while True:
            c = f.readline()
            if newCount % 10000 == 0:
                print("Compressing - " + str((newCount * 100) / total_number_of_lines))
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
            line_words_pos_dict = {}

            line_all_words = {}
            words_in_line = re.findall(r'\w+', c)
            for word in words_in_line:
                if word in nodes_dict_words:
                    line_all_words[word] = nodes_dict_words[word]


            for key, value in line_all_words.items():
                cursor = 0
                index:int = c.find(key, cursor)
                while index != -1:
                    if index in line_words_pos_dict.keys():
                        if len(line_words_pos_dict[index].character) < len(value.character):
                            line_words_pos_dict[index] = value
                    else:
                        line_words_pos_dict[index] = value
                    cursor = cursor + len(value.character)
                    index: int = c.find(key, cursor)

            iter_index = 0
            while iter_index < len(c):
                if iter_index in line_words_pos_dict.keys():
                    encoded_contents = encoded_contents + line_words_pos_dict[iter_index].encoded_string

                    iter_index = iter_index + len(line_words_pos_dict[iter_index].character)
                else:
                    encoded_contents = encoded_contents + nodes_dict_chars[c[iter_index]].encoded_string

                    iter_index = iter_index + 1

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
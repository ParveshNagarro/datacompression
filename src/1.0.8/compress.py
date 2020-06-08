import io
import pickle
import re
import sys

class Node:
    character: str
    encoded_string: str
    frequency: int
    children: []
    final_children_dict: {}

    def __init__(self, character: str, frequency: int):
        self.character = character
        self.frequency = frequency
        self.children = []
        self.encoded_string = ""

class Child:
    node_character: str
    encoded_string: str
    frequency: int
    children: []

    def __init__(self, node_character: str, frequency: int):
        self.node_character = node_character
        self.frequency = frequency
        self.children = []
        self.encoded_string = ""


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


nodes_dict_chars = []
with open("../../data/tmp/enwik8_dict_chars", 'rb') as f:
    nodes_dict_chars = pickle.load(f)

nodes_dict_words = []
with open("../../data/tmp/enwik8_dict_words", 'rb') as f:
    nodes_dict_words = pickle.load(f)

final_dict_of_all_nodes={}
with open("../../data/tmp/enwik8_final_model", 'rb') as f:
    final_dict_of_all_nodes = pickle.load(f)

encoded_contents = ""

print("Reading the dicts is complete, it's time to write the file back.")
enwik_output: str = "../../data/tmp/enwik8_compressed"
print("The compressed version will be written to " + enwik_output)
cutoff = 0

enwik: str = "../../data/tmp/enwik8"
count = 100000000

root: Node = None
pointer_parent = None
pointer: Node = None

newCount = 0
total_number_of_lines = 1128024
print("doing the compression")
with open(enwik_output, "w+b") as fo:
    with open(enwik, "r", encoding="utf-8") as f:
        while True:
            c = f.readline()
            if newCount % 1000 == 0:
                print("Compressing - " + str((newCount * 100) / total_number_of_lines))
            newCount = newCount + 1
            if not c:

                if pointer is not None:
                    if pointer.character in pointer_parent.final_children_dict:
                        encoded_contents = encoded_contents + pointer_parent.final_children_dict[
                            pointer.character].encoded_string
                    else:
                        # break everything down :P
                        print("something is wrong 3")
                        sys.exit()

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

            #map<index of char, node>
            line_words_pos_dict = {}

            iterator = re.compile(r'\w+').finditer(c)
            for match in iterator:
                 word = match.group()
                 if word in nodes_dict_words:
                    line_words_pos_dict[match.start()] = final_dict_of_all_nodes[match.group()]


            iter_index = 0
            while iter_index < len(c):
                current_node = None
                if iter_index in line_words_pos_dict.keys():
                    current_node = line_words_pos_dict[iter_index]
                    iter_index = iter_index + len(line_words_pos_dict[iter_index].character)
                else:
                    current_node = final_dict_of_all_nodes[c[iter_index]]
                    iter_index = iter_index + 1

                if root is None:
                    root = current_node
                    pointer_parent = current_node
                elif pointer is None:
                    pointer = current_node
                else :
                    if len(pointer_parent.character) > 1 and pointer.character == " " and len(
                            current_node.character) > 1:
                        if current_node.character in pointer_parent.final_children_dict:
                            encoded_contents = encoded_contents + pointer_parent.final_children_dict[current_node.character].encoded_string
                        else:
                            #break everything down :P
                            print("something is wrong 1")
                            sys.exit()

                        pointer = None
                        pointer_parent = final_dict_of_all_nodes[pointer_parent.final_children_dict[current_node.character].node_character]
                    else:
                        if pointer.character in pointer_parent.final_children_dict:
                            encoded_contents = encoded_contents + pointer_parent.final_children_dict[pointer.character].encoded_string
                        else:
                            #break everything down :P
                            print("something is wrong 2")
                            sys.exit()

                        pointer_parent = pointer
                        pointer = current_node

            while len(encoded_contents) > 8:
                bytes_array = []
                string_to_write = encoded_contents[:8]
                encoded_contents = encoded_contents[8:]
                bytes_array.append(int(string_to_write, 2))
                fo.write(bytearray(bytes_array))

print("cutoff" + str(cutoff))
with open("../../data/tmp/enwik8_cutoff", 'wb') as f:
    # Pickle the 'data' dictionary using the highest protocol available.
    pickle.dump(cutoff, f, pickle.HIGHEST_PROTOCOL)
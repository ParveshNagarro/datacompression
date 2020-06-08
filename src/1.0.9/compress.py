import io
import pickle
import re
import sys


class Node:
    character: str
    frequency: int
    children: []
    final_children_dict: {}
    children_rare: []
    final_children_dict_rare: {}
    is_rare_children_node:bool

    def __init__(self, character: str, frequency: int):
        self.character = character
        self.frequency = frequency
        self.children = []
        self.encoded_string = ""
        self.final_children_dict = {}
        self.final_children_dict_rare: {}
        self.is_rare_children_node = False


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


def append_the_child_node(huffman_tree_node: Child, nodes_collect: {}):
    if len(huffman_tree_node.children) > 0:
        append_the_child_node(huffman_tree_node.children[0], nodes_collect)
        if (len(huffman_tree_node.children)) > 1:
            append_the_child_node(huffman_tree_node.children[1], nodes_collect)
    else:
        nodes_collect[huffman_tree_node.node_character] = huffman_tree_node


def huffman_iteration(huffman_tree_to_iterate):
    # print("Sorting the nodes in the tree. Right now there are " + str(len(huffman_tree_to_iterate)) + " nodes.")
    huffman_tree_to_iterate.sort(key=lambda x: x.frequency, reverse=False)
    node1 = huffman_tree_to_iterate.pop(0)
    node2 = huffman_tree_to_iterate.pop(0)
    # print("Creating a new node with characters " + node1.character + node2.character + "  and string " + str(
    # node1.frequency + node2.frequency))
    new_node = Child("", node1.frequency + node2.frequency)
    new_node.children.append(node1)
    new_node.children.append(node2)
    huffman_tree_to_iterate.append(new_node)
    # print("Sorting the nodes in the tree. Right now there are " + str(len(huffman_tree_to_iterate)) + " nodes.")
    huffman_tree_to_iterate.sort(key=lambda x: x.frequency, reverse=False)


def encode_the_node(node):
    if node.children is not None and 0 < len(node.children):
        # print("Encoding the node " + str(node.frequency) + "-" + node.character)
        # print("Now encoding the first child of the node + " + str(node.frequency) + "-" + node.character)
        node.children[0].encoded_string = node.encoded_string + "0"
        encode_the_node(node.children[0])
        if len(node.children) > 1:
            # print("Now encoding the second child of the node + " + str(node.frequency) + "-" + node.character)
            node.children[1].encoded_string = node.encoded_string + "1"
            encode_the_node(node.children[1])



def build_children_huffman(value):
    #print("building huffman trees for " + key + " containing " + str(len(value.final_children_dict)) + " nodes and it's " )
    if len(value.final_children_dict) > 1:
        children_to_build_a_tree = []
        for child_node in list(value.final_children_dict.values()):
            children_to_build_a_tree.append(child_node)

        children_to_build_a_tree.sort(key=lambda x: x.frequency, reverse=False)
        while len(children_to_build_a_tree) > 1:
            huffman_iteration(children_to_build_a_tree)

        encode_the_node(children_to_build_a_tree[0])

        value.children = children_to_build_a_tree

        nodes_dict_children = {}
        append_the_child_node(children_to_build_a_tree[0], nodes_dict_children)
        value.final_children_dict = nodes_dict_children

    elif len(value.final_children_dict) == 1:
        child_key = next(iter(value.final_children_dict))
        new_node = Child("", value.final_children_dict[child_key].frequency)
        new_node.children.append(value.final_children_dict[child_key])
        value.final_children_dict[child_key].encoded_string = "0"
        value.children.append(new_node)

        nodes_dict_children = {}
        append_the_child_node(value.children[0], nodes_dict_children)

        value.final_children_dict = nodes_dict_children


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

rare_chars_root = final_dict_of_all_nodes["Rare_characters_aboch8663"]

root: Node = None
pointer_parent = None
pointer: Node = None

newCount = 0
total_number_of_lines = 1128024

enwik8_temp_refresh = {}

pointer_string = ""
pointer_parent_string = ""
current_node_string = ""

print("doing the compression")
with open(enwik_output, "w+b") as fo:
    with open(enwik, "r", encoding="utf-8") as f:
        while True:
            c = f.readline()
            if newCount % 10000 == 0:
                print("Compressing - " + str((newCount * 100) / total_number_of_lines))
                print("building huffman trees for " + str(len(enwik8_temp_refresh)) + " nodes and it's ")
                #for key, value in enwik8_temp_refresh.items():
                 #   build_children_huffman(value)
                enwik8_temp_refresh = {}

                print("done")
            newCount = newCount + 1
            if not c:

                if pointer is not None:
                    if pointer.character in pointer_parent.final_children_dict:
                        encoded_contents = encoded_contents + pointer_parent.final_children_dict[
                            pointer.character].encoded_string
                        if pointer.is_rare_children_node is True:
                            encoded_contents = encoded_contents + pointer.final_children_dict_rare[pointer_string].encoded_string
                        pointer_parent.final_children_dict[pointer.character].frequency = pointer_parent.final_children_dict[pointer.character].frequency - 1
                        enwik8_temp_refresh[pointer_parent.character] = pointer_parent
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
                    current_node_string = current_node.character
                elif c[iter_index] in final_dict_of_all_nodes:
                    current_node = final_dict_of_all_nodes[c[iter_index]]
                    current_node_string = c[iter_index]
                    iter_index = iter_index + 1
                else:
                    current_node = rare_chars_root
                    current_node_string = c[iter_index]
                    iter_index = iter_index + 1

                if root is None:
                    root = current_node
                    pointer_parent = current_node
                    pointer_parent_string = current_node_string
                elif pointer is None:
                    pointer = current_node
                    pointer_string = current_node_string
                else :
                    if len(pointer_parent.character) > 1 and pointer_parent.is_rare_children_node is False and pointer.character == " " and len(current_node.character) > 1 and current_node.is_rare_children_node is False:
                        if current_node.character in pointer_parent.final_children_dict:
                            encoded_contents = encoded_contents + pointer_parent.final_children_dict[current_node.character].encoded_string
                            pointer_parent.final_children_dict[current_node.character].frequency = pointer_parent.final_children_dict[current_node.character].frequency - 1
                            enwik8_temp_refresh[pointer_parent.character] = pointer_parent
                        else:
                            #break everything down :P
                            print("something is wrong 1")
                            sys.exit()

                        pointer = None
                        pointer_parent = final_dict_of_all_nodes[pointer_parent.final_children_dict[current_node.character].node_character]
                    else:
                        if pointer.character in pointer_parent.final_children_dict:
                            encoded_contents = encoded_contents + pointer_parent.final_children_dict[pointer.character].encoded_string
                            if pointer.is_rare_children_node is True:
                                encoded_contents = encoded_contents + pointer.final_children_dict_rare[pointer_string].encoded_string
                            pointer_parent.final_children_dict[pointer.character].frequency = pointer_parent.final_children_dict[pointer.character].frequency - 1
                            enwik8_temp_refresh[pointer_parent.character] = pointer_parent
                        else:
                            #break everything down :P
                            print("something is wrong 2")
                            sys.exit()

                        pointer_parent = pointer
                        pointer = current_node
                        pointer_parent_string = pointer_string
                        pointer_string = current_node_string

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

with open("../../data/tmp/enwik8_final_model_post_compression", 'wb') as f:
    # Pickle the 'data' dictionary using the highest protocol available.
    pickle.dump(final_dict_of_all_nodes, f, pickle.HIGHEST_PROTOCOL)
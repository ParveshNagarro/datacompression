import io
import pickle
import re


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

def huffman_iteration_node(huffman_tree_to_iterate):
    print("Sorting the nodes in the tree. Right now there are " + str(len(huffman_tree_to_iterate)) + " nodes.")
    huffman_tree_to_iterate.sort(key=lambda x: x.frequency, reverse=False)
    node1 = huffman_tree_to_iterate.pop(0)
    node2 = huffman_tree_to_iterate.pop(0)
    print("Creating a new node with characters " + node1.character + node2.character + "  and string " + str(node1.frequency + node2.frequency))
    new_node = Node(node1.character + node2.character, node1.frequency + node2.frequency)
    new_node.children.append(node1)
    new_node.children.append(node2)
    huffman_tree_to_iterate.append(new_node)
    print("Sorting the nodes in the tree. Right now there are " + str(len(huffman_tree_to_iterate)) + " nodes.")
    huffman_tree_to_iterate.sort(key=lambda x: x.frequency, reverse=False)


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


#    else:
# print("Nothing to encode in this node as there are either no children")


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


def build_children_huffman(value):
    print("building huffman trees for " + key + " containing " + str(len(value.final_children_dict)) + " nodes and it's " + str(count_pointer_huff_trees) + " out of " + number_of_huffman_trees)
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


# ------------New compression starts here --------


nodes_dict_chars = {}
with open("../../data/tmp/enwik8_dict_chars", 'rb') as f:
    nodes_dict_chars = pickle.load(f)

nodes_dict_words = {}
with open("../../data/tmp/enwik8_dict_words", 'rb') as f:
    nodes_dict_words = pickle.load(f)


nodes_dict_chars_rare = {}
with open("../../data/tmp/enwik8_dict_chars_rare", 'rb') as f:
    nodes_dict_chars_rare = pickle.load(f)

print("Reading the dicts is complete, it's time to write the file back.")

rare_chars_root = Node("Rare_characters_aboch8663", 1)
rare_chars_root.is_rare_children_node = True
rare_chars_root.final_children_dict_rare = nodes_dict_chars_rare

nodes_list_chars_rare = []
for key, value in nodes_dict_chars_rare.items():
    nodes_list_chars_rare.append(value)

nodes_list_chars_rare.sort(key=lambda x: x.frequency, reverse=False)
while len(nodes_list_chars_rare) > 1:
    huffman_iteration_node(nodes_list_chars_rare)

encode_the_node(nodes_list_chars_rare[0])

rare_chars_root.children_rare = nodes_list_chars_rare


root: Node = None
pointer_parent = None
pointer: Node = None

newCount = 0
total_number_of_lines = 1128024

final_dict_of_all_nodes = {}

enwik: str = "../../data/tmp/enwik8"
print("doing the compression")
with open(enwik, "r", encoding="utf-8") as f:
    while True:
        c = f.readline()
        if newCount % 1000 == 0:
            print("Compressing - " + str((newCount * 100) / total_number_of_lines))
        newCount = newCount + 1

        if not c:
            print("End of file. writing what ever is left")
            break

        # map<index of char, node>
        line_words_pos_dict = {}

        iterator = re.compile(r'\w+').finditer(c)
        for match in iterator:
            word = match.group()
            if word in nodes_dict_words:
                line_words_pos_dict[match.start()] = nodes_dict_words[match.group()]

        iter_index = 0
        while iter_index < len(c):
            current_node = None
            if iter_index in line_words_pos_dict.keys():
                current_node = line_words_pos_dict[iter_index]
                iter_index = iter_index + len(line_words_pos_dict[iter_index].character)
            elif c[iter_index] in nodes_dict_chars:
                current_node = nodes_dict_chars[c[iter_index]]
                iter_index = iter_index + 1
            else:
                current_node = rare_chars_root
                iter_index = iter_index + 1

            final_dict_of_all_nodes[current_node.character] = current_node

            if root is None:
                root = current_node
                pointer_parent = current_node
            elif pointer is None:
                pointer = current_node
            else:
                if len(pointer_parent.character) > 1 and pointer_parent.is_rare_children_node is False and pointer.character == " " and len(current_node.character) > 1 and current_node.is_rare_children_node is False:
                    if current_node.character in pointer_parent.final_children_dict:
                        childToUse = pointer_parent.final_children_dict[current_node.character]
                        childToUse.frequency = childToUse.frequency + 1
                    else:
                        childToUse = Child(current_node.character, 1)
                        pointer_parent.final_children_dict[current_node.character] = childToUse

                    pointer = None
                    pointer_parent = current_node
                else:
                    if pointer.character in pointer_parent.final_children_dict:
                        childToUse = pointer_parent.final_children_dict[pointer.character]
                        childToUse.frequency = childToUse.frequency + 1
                    else:
                        childToUse = Child(pointer.character, 1)
                        pointer_parent.final_children_dict[pointer.character] = childToUse

                    pointer_parent = pointer
                    pointer = current_node



if pointer is not None:
    if pointer.character in pointer_parent.final_children_dict:
        childToUse = pointer_parent.final_children_dict[pointer.character]
        childToUse.frequency = childToUse.frequency + 1
    else:
        childToUse = Child(pointer.character, 1)
        pointer_parent.final_children_dict[pointer.character] = childToUse


number_of_huffman_trees = str(len(final_dict_of_all_nodes))
print("the number of huffman trees to build is " + str(len(final_dict_of_all_nodes)))

count_pointer_huff_trees = 0
for key, value in final_dict_of_all_nodes.items():
    build_children_huffman(value)
    print("huffman trees build " + str(count_pointer_huff_trees) + " out of " + number_of_huffman_trees)
    count_pointer_huff_trees = count_pointer_huff_trees + 1

with open("../../data/tmp/enwik8_final_model", 'wb') as f:
    # Pickle the 'data' dictionary using the highest protocol available.
    pickle.dump(final_dict_of_all_nodes, f, pickle.HIGHEST_PROTOCOL)

with open("../../data/tmp/enwik8_first_node", 'wb') as f:
    # Pickle the 'data' dictionary using the highest protocol available.
    pickle.dump(root.character, f, pickle.HIGHEST_PROTOCOL)

# ------------New compression starts ends here --------
import io
import pickle
import re

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


class Child :
    node: Node
    encoded_string: str
    frequency: int
    children: []

    def __init__(self, node: Node, frequency: int):
        self.node = node
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


def append_the_child_node(huffman_tree_node: Child, nodes_collect:{}):
    if len(huffman_tree_node.children) > 0:
        append_the_child_node(huffman_tree_node.children[0], nodes_collect)
        if (len(huffman_tree_node.children)) > 1:
            append_the_child_node(huffman_tree_node.children[1], nodes_collect)
    else:
        nodes_collect[huffman_tree_node.node.character] = huffman_tree_node


def huffman_iteration(huffman_tree_to_iterate):
    #print("Sorting the nodes in the tree. Right now there are " + str(len(huffman_tree_to_iterate)) + " nodes.")
    huffman_tree_to_iterate.sort(key=lambda x: x.frequency, reverse=False)
    node1 = huffman_tree_to_iterate.pop(0)
    node2 = huffman_tree_to_iterate.pop(0)
    #print("Creating a new node with characters " + node1.character + node2.character + "  and string " + str(
       # node1.frequency + node2.frequency))
    new_node = Child(None, node1.frequency + node2.frequency)
    new_node.children.append(node1)
    new_node.children.append(node2)
    huffman_tree_to_iterate.append(new_node)
    #print("Sorting the nodes in the tree. Right now there are " + str(len(huffman_tree_to_iterate)) + " nodes.")
    huffman_tree_to_iterate.sort(key=lambda x: x.frequency, reverse=False)


def encode_the_node(node):

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
        #print("Nothing to encode in this node as there are either no children")


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

# ------------New compression starts here --------


huffman_tree_chars = []
with open("../../data/tmp/enwik8_dict_chars", 'rb') as f:
    huffman_tree_chars = pickle.load(f)

huffman_tree_words = []
with open("../../data/tmp/enwik8_dict_words", 'rb') as f:
    huffman_tree_words = pickle.load(f)

nodes_dict_words = {}
append_the_node(huffman_tree_words[0], nodes_dict_words)

nodes_dict_chars = {}
append_the_node(huffman_tree_chars[0], nodes_dict_chars)

print("Reading the dicts is complete, it's time to write the file back.")

root:Node = None
pointer:Node = None

newCount = 0
total_number_of_lines = 1128024

final_dict_of_all_nodes = {}

enwik: str = "../../data/tmp/enwik8"
print("doing the compression")
with open(enwik, "r", encoding="utf-8") as f:
    while True:
        c = f.readline()
        if newCount % 100 == 0:
            print("Compressing - " + str((newCount * 100) / total_number_of_lines))
        newCount = newCount + 1

        if not c:
            print("End of file. writing what ever is left")
            break

        # map<index of char, node>
        line_words_pos_dict = {}

        nodes_dict_words_in_this_line = {}

        # separating out the words used in this line and adding them to the final list as well
        words = re.findall(r'\w+', c)
        for word in words:
            if word in nodes_dict_words:
                nodes_dict_words_in_this_line[word] = nodes_dict_words[word]

        for key, value in nodes_dict_words_in_this_line.items():
            cursor = 0
            index: int = c.find(key, cursor)
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
            current_node = None
            if iter_index in line_words_pos_dict.keys():
                current_node = line_words_pos_dict[iter_index]
                iter_index = iter_index + len(line_words_pos_dict[iter_index].character)
            else:
                current_node = nodes_dict_chars[c[iter_index]]
                iter_index = iter_index + 1

            final_dict_of_all_nodes[current_node.character] = current_node
            if root is None:
                root = current_node
                pointer = current_node
            else :
                childToUse = None
                for child in pointer.children:
                    if child.node.character == current_node.character:
                        child.frequency = child.frequency + 1
                        childToUse = child

                if childToUse is None:
                    childToUse = Child(current_node, 1)
                    pointer.children.append(childToUse)

                pointer = childToUse.node

number_of_huffman_trees = str(len(final_dict_of_all_nodes))
print("the number of huffman trees to build is " + str(len(final_dict_of_all_nodes)))

count_pointer_huff_trees = 0
for key, value in final_dict_of_all_nodes.items():
    if len(value.children) > 1:
        children_to_build_a_tree = []
        for child_node in value.children:
            children_to_build_a_tree.append(child_node)

        children_to_build_a_tree.sort(key=lambda x: x.frequency, reverse=False)
        while len(children_to_build_a_tree) > 1:
            huffman_iteration(children_to_build_a_tree)

        encode_the_node(children_to_build_a_tree[0])

        value.children = children_to_build_a_tree

        nodes_dict_children = {}
        append_the_child_node(children_to_build_a_tree[0], nodes_dict_children)
        value.final_children_dict = nodes_dict_children

    elif len(value.children) == 1:

        new_node = Child(None, value.children[0].frequency)
        new_node.children.append(value.children[0])
        value.children[0].encoded_string = "0"
        value.children[0]=new_node

        nodes_dict_children = {}
        append_the_child_node(value.children[0], nodes_dict_children)

        value.final_children_dict = nodes_dict_children

    print("huffman trees build " + str(count_pointer_huff_trees) + " out of " + number_of_huffman_trees)
    count_pointer_huff_trees = count_pointer_huff_trees + 1

with open("../../data/tmp/enwik8_final_model", 'wb') as f:
    # Pickle the 'data' dictionary using the highest protocol available.
    pickle.dump(final_dict_of_all_nodes, f, pickle.HIGHEST_PROTOCOL)

with open("../../data/tmp/enwik8_first_node", 'wb') as f:
    # Pickle the 'data' dictionary using the highest protocol available.
    pickle.dump(root.character, f, pickle.HIGHEST_PROTOCOL)



# ------------New compression starts ends here --------
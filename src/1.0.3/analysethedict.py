import io
import pickle


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


def append_the_node(huffman_tree_node: Node, nodes_collect:[]):
    if len(huffman_tree_node.children) > 0:
        append_the_node(huffman_tree_node.children[0], nodes_collect)
        if (len(huffman_tree_node.children)) > 1:
            append_the_node(huffman_tree_node.children[1], nodes_collect)
    else:
        nodes_collect.append(huffman_tree_node)


def primary_true(node:Node):
    return node.frequency >= 3047318


# the program starts heref

huffman_tree = []
with open("../../data/tmp/enwik8_dict", 'rb') as f:
    huffman_tree = pickle.load(f)

cutoff_in = 0
cutoff = 0
with open("../../data/tmp/enwik8_cutoff", 'rb') as f:
    cutoff_in = pickle.load(f)


nodes_list = []
append_the_node(huffman_tree[0], nodes_list)
nodes_list.sort(key=lambda x: x.frequency, reverse=True)
count = 1
total_count = 100000000
with open("../../data/tmp/enwik8__dict_analysis", 'w', encoding="utf-8") as f:
    for node_to_print in nodes_list:
        f.write(node_to_print.character + " - " + str(node_to_print.frequency) + " - " + node_to_print.encoded_string + " - " + str((node_to_print.frequency * 100)/total_count))
        f.write("\n")
        count = count + 1


nodes_list_primary = []

for node_to_print in nodes_list:
    if (primary_true(node_to_print)) :
        nodes_list_primary.append(node_to_print)

count = 1
total_count = 100000000
with open("../../data/tmp/enwik8__dict_analysis_primary_dict", 'w', encoding="utf-8") as f:
    for node_to_print in nodes_list_primary:
        f.write(node_to_print.character + " - " + str(node_to_print.frequency) + " - " + node_to_print.encoded_string + " - " + str((node_to_print.frequency * 100)/total_count))
        f.write("\n")
        count = count + 1




print("Put'em all in a second list of nodes that will become a huffman eventually")
huffman_tree = []
for  value in nodes_list_primary:
    huffman_tree.append(value)

print("Iterating and merging the nodes until only one remains")
while len(huffman_tree) > 1:
    huffman_iteration(huffman_tree)

encode_the_node(huffman_tree[0])

nodes_list_primary_updated = []
append_the_node(huffman_tree[0], nodes_list_primary_updated)
nodes_list_primary_updated.sort(key=lambda x: x.frequency, reverse=True)


count = 1
total_count = 100000000
with open("../../data/tmp/enwik8__dict_analysis_primary_dict_updated", 'w', encoding="utf-8") as f:
    for node_to_print in nodes_list_primary:
        f.write(node_to_print.character + " - " + str(node_to_print.frequency) + " - " + node_to_print.encoded_string + " - " + str((node_to_print.frequency * 100)/total_count))
        f.write("\n")
        count = count + 1

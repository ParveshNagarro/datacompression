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
    print("Creating a new node with characters " + node1.character + node2.character + "  and string " + str(node1.frequency + node2.frequency))
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
    if  node.children is not None and 0 < len(node.children):
        string_to_print += "-> \n\t"
        string_to_print += print_a_node(node.children[0]) + " , "
        if len(node.children) > 1:
            string_to_print += print_a_node(node.children[1])
    return string_to_print


def print_a_list(nodes_list_to_print):
    print("printing a list")
    for node_to_print in nodes_list_to_print:
        print(print_a_node(node_to_print))


# the program starts here

print("Here goes nothing!!!")

enwik: str = "../../data/tmp/enwik8"
print("Reading the file " + enwik)

with open(enwik, "r", encoding="utf-8") as f:
    print("The current approach is stupid, so reading the entire file into one string")
    contents = f.read()
    print("The contents of the file are " + contents)
    print(contents)

print("Creating a frequency distribution dict of the data")
nodes_dict = {}
for letter in contents:
    if letter in  nodes_dict:
        node: Node = nodes_dict[letter]
        node.frequency = node.frequency + 1
    else:
        node = Node(letter , 1)
        nodes_dict[letter] = node

print("Converting the dict into a list of nodes")
nodes_list = []
for key, value in nodes_dict.items():
    nodes_list.append(value)
nodes_list.sort(key=lambda x: x.frequency, reverse=False)

print("The entire contents after the sorting and node creations")
print_a_list(nodes_list)

print("Put'em all in a second list of nodes that will become a huffman eventually")
huffman_tree = []
for key, value in nodes_dict.items():
    huffman_tree.append(value)

print("Iterating and merging the nodes until only one remains")
while len(huffman_tree) > 1:
    huffman_iteration(huffman_tree)
print_a_list(huffman_tree)

encode_the_node(huffman_tree[0])
print_a_list(nodes_list)

encoded_contents = ""

print("converting the contents of the string input")
for c in contents:
  #  print(c + "-" + node_map[c])
    encoded_contents = encoded_contents + nodes_dict[c].encoded_string

print("input string")
print(contents)
print("input content length (bytes)" + str(len(contents)))

print("output string")
print(encoded_contents)
print("output content length (bits)" + str(len(encoded_contents)))
print("writing output")

print("Reading and the conversion is complete, it's time to write the file back.")
enwik_output: str = "../../data/tmp/enwik8_compressed"
print("The compressed version will be written to " + enwik_output)

with open(enwik_output, "w+b") as f:

    print("writing out the contents to the output file")
    bytes_array = []
    cutoff = 0
    while len(encoded_contents) > 0:
        if len(encoded_contents) > 8:
            string_to_write = encoded_contents[:8]
            encoded_contents = encoded_contents[8:]
            print(int(string_to_write, 2))
            bytes_array.append(int(string_to_write, 2))
            print(hex(int(string_to_write, 2)))
            print(string_to_write)

        else:
            string_to_write = encoded_contents
            encoded_contents = ""
            cutoff = 8  - len(string_to_write)
            bytes_array.append(int(string_to_write, 2))
            string_to_write = encoded_contents + ("0" * cutoff)
            print(int(string_to_write, 2))
            print(hex(int(string_to_write, 2)))
            print(string_to_write)
            print(cutoff)

    f.write(bytearray(bytes_array))
    print(bytes_array)


with open("../../data/tmp/enwik8_dict", 'wb') as f:
    # Pickle the 'data' dictionary using the highest protocol available.
    pickle.dump(huffman_tree, f, pickle.HIGHEST_PROTOCOL)

with open("../../data/tmp/enwik8_cutoff", 'wb') as f:
    # Pickle the 'data' dictionary using the highest protocol available.
    pickle.dump(cutoff, f, pickle.HIGHEST_PROTOCOL)

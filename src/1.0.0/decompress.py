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


def huffman_iteration(huffman_tree):
    huffman_tree.sort(key=lambda x: x.frequency, reverse=False)
    node1 = huffman_tree.pop(0)
    node2 = huffman_tree.pop(0)
    newNode = Node(node1.character + node2.character, node1.frequency + node2.frequency)
    newNode.children.append(node1)
    newNode.children.append(node2)
    huffman_tree.append(newNode)
    huffman_tree.sort(key=lambda x: x.frequency, reverse=False)


def encode_theNode(node):
    string_to_print = str(node.frequency) + "-" + node.character
    if node.children is not None and 0 < len(node.children):
        node.children[0].encoded_string = node.encoded_string + "0"
        encode_theNode(node.children[0])
        if len(node.children) > 1:
            node.children[1].encoded_string = node.encoded_string + "1"
            encode_theNode(node.children[1])


def print_a_node(node):
    string_to_print = str(node.frequency) + "-" + node.character + "-" + node.encoded_string
    if  node.children is not None and 0 < len(node.children):
        string_to_print += "-> \n\t"
        string_to_print += print_a_node(node.children[0]) + " , "
        if len(node.children) > 1:
            string_to_print += print_a_node(node.children[1])
    return string_to_print


def print_a_list(nodes_list):
    print("printing a list")
    for node in nodes_list:
        print(print_a_node(node))


# the program starts here

enwik: str = "../../data/tmp/enwik8"
f= open(enwik, "r", encoding="utf-8")
contents = f.read()
print(contents)
f.close();



nodes_dict = {}
for letter in contents:
    if letter in  nodes_dict:
        node: Node = nodes_dict[letter]
        node.frequency = node.frequency + 1
    else:
        node = Node(letter , 1)
        nodes_dict[letter] = node

nodes_list = []
for key, value in nodes_dict.items():
    nodes_list.append(value)

nodes_list.sort(key=lambda x: x.frequency, reverse=False)

#print_a_list(nodes_list)

huffman_tree = []
for key, value in nodes_dict.items():
    huffman_tree.append(value)

while len(huffman_tree) > 1:
    huffman_iteration(huffman_tree)
 #   print_a_list(huffman_tree)

encode_theNode(huffman_tree[0])
#print_a_list(nodes_list)

node_map  = {node.character : node.encoded_string for node in nodes_list}

print(node_map)

decoded_contents = ""
with open("../../data/tmp/enwik8o", "rb") as f:
    byte = f.read(1)
    while byte != b"":
        # Do stuff with byte.
        decoded_contents = decoded_contents + "{0:b}".format(ord(byte))
        byte = f.read(1)

print(decoded_contents)

output_final = ""
parent_node = huffman_tree[0]
current_node = parent_node
for character in decoded_contents:
    if character == "1":
        current_node = current_node.children[1]
    else:
        current_node = current_node.children[0]

    if len(current_node.children) == 0:
        output_final = output_final + current_node.character
        current_node = parent_node

print(output_final)

with open("../../data/tmp/enwik8_output", "w", encoding="utf-8") as f:
    f.write(output_final)

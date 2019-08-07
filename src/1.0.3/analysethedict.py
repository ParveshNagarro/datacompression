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



def append_the_node(huffman_tree_node: Node, nodes_collect:{}):
    if len(huffman_tree_node.children) > 0:
        append_the_node(huffman_tree_node.children[0], nodes_collect)
        if (len(huffman_tree_node.children)) > 1:
            append_the_node(huffman_tree_node.children[1], nodes_collect)
    else:
        nodes_collect[huffman_tree_node.character] = huffman_tree_node



huffman_tree_chars = []
with open("../../data/tmp/enwik8_dict_chars", 'rb') as f:
    huffman_tree_chars = pickle.load(f)

huffman_tree_words = []
with open("../../data/tmp/enwik8_dict_words", 'rb') as f:
    huffman_tree_words = pickle.load(f)

huffman_tree = []

root_node:Node = Node("root", 0)
root_node.children.append(huffman_tree_chars[0])
root_node.children.append(huffman_tree_words[0])

huffman_tree.append(root_node)

encode_the_node(huffman_tree[0])

word_nodes_dict = {}
append_the_node(huffman_tree_words[0], word_nodes_dict)

word_nodes_list = []
for key, value in word_nodes_dict.items():
    word_nodes_list.append(value)
word_nodes_list.sort(key=lambda x: x.frequency)



char_nodes_dict = {}
append_the_node(huffman_tree_chars[0], char_nodes_dict)

char_nodes_list = []
for key, value in char_nodes_dict.items():
    char_nodes_list.append(value)
char_nodes_list.sort(key=lambda x: x.frequency)

with open("../../data/tmp/analysis/enwik8_dict__words", 'w', encoding="utf-8") as f:
    # Pickle the 'data' dictionary using the highest protocol available.
    for value in word_nodes_list:
        f.write(value.character + " - " + str(value.frequency) + " - " + value.encoded_string + "\n")



with open("../../data/tmp/analysis/enwik8_dict__chars", 'w', encoding="utf-8") as f:
    # Pickle the 'data' dictionary using the highest protocol available.
    for value in char_nodes_list:
        f.write(value.character + " - " + str(value.frequency) + " - " + value.encoded_string + "\n")


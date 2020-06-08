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


nodes_dict_chars = []
with open("../../data/tmp/enwik8_dict_chars", 'rb') as f:
    nodes_dict_chars = pickle.load(f)

nodes_dict_words = []
with open("../../data/tmp/enwik8_dict_words", 'rb') as f:
    nodes_dict_words = pickle.load(f)

final_dict_of_all_nodes={}
with open("../../data/tmp/enwik8_final_model", 'rb') as f:
    final_dict_of_all_nodes = pickle.load(f)


count_pointer_huff_trees = 0
with open("../../data/tmp/analysis/chars_freqs", "w", encoding="utf-8") as f0:
    for key, value in final_dict_of_all_nodes.items():
        f0.write(key + "\t" + str(len(value.final_children_dict)) + "\n")

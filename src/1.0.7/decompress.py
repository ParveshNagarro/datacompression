import io
import pickle


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


huffman_tree_chars = []
with open("../../data/tmp/enwik8_dict_chars", 'rb') as f:
    huffman_tree_chars = pickle.load(f)

huffman_tree_words = []
with open("../../data/tmp/enwik8_dict_words", 'rb') as f:
    huffman_tree_words = pickle.load(f)

final_dict_of_all_nodes={}
with open("../../data/tmp/enwik8_final_model", 'rb') as f:
    final_dict_of_all_nodes = pickle.load(f)

cutoff_in = 0
cutoff = 0
with open("../../data/tmp/enwik8_cutoff", 'rb') as f:
    cutoff_in = pickle.load(f)

first_word = ""
with open("../../data/tmp/enwik8_first_node", 'rb') as f:
    first_word = pickle.load(f)

output_final = "" + first_word
parent_node = final_dict_of_all_nodes[first_word]
current_node = parent_node
decoded_string = ""

total_count = 100000000
newCount = 0
with open("../../data/tmp/enwik8_output", "w", encoding="utf-8") as f0:
    with open("../../data/tmp/enwik8_compressed", "rb") as f:
        byte = f.read(1)
        while byte != b"":
            # Do stuff with byte.
            newCount = newCount + 1
            if newCount % 1000000 == 0:
                print("percentage of file read" + str((newCount * 100) / total_count))

            byte_temp = byte
            byte = f.read(1)
            decoded_string = "{0:b}".format(ord(byte_temp))

            cutoff = 8 - len(decoded_string)
            if byte == b"":
                cutoff = cutoff - cutoff_in
                if cutoff < 0:
                    cutoff = 0

            decoded_string = ("0" * cutoff) + decoded_string

            tmp_decoding_string = decoded_string
            for character in tmp_decoding_string:
                if isinstance(current_node, Node):
                    if character == "1":
                        current_node = current_node.children[0].children[1]
                    else:
                        current_node = current_node.children[0].children[0]
                else:
                    if character == "1":
                        current_node = current_node.children[1]
                    else:
                        current_node = current_node.children[0]

                if len(current_node.children) == 0:
                    output_final = output_final + current_node.node_character
                    current_node = final_dict_of_all_nodes[current_node.node_character]
                    if len(output_final) > 8:
                        tmp_output_final = output_final[:8]
                        output_final = output_final[8:]
                        f0.write(tmp_output_final)

        if len(output_final) > 0:
            f0.write(output_final)



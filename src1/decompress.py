import io
import pickle

#ENWIK_FILENAME = "../data/test.txt"
ENWIK_FILENAME = "../data/enwik9"
NUMBER_OF_LINES =  13147026

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


def convert_huffman_map_to_tree(huffman_map_input):
    result_huffman_tree = []
    root = Node("root", 1)
    result_huffman_tree.append(root)

    for key, value in huffman_map_input.items():
        current_node = root
        for character_huff in value[:-1]:

            child_node_found = None
            for child_node_to_check in current_node.children:
                if child_node_to_check.character == character_huff:
                    child_node_found = child_node_to_check

            if child_node_found is not None:
                current_node = child_node_found
            else:
                tmp_node = Node(character_huff, 1)
                if character_huff == "1":
                    current_node.children.insert(1, tmp_node)
                else:
                    current_node.children.insert(0, tmp_node)
                current_node = tmp_node

        new_node = Node(key, 1)
        new_node.encoded_string = value
        if value[-1] == "1":
            current_node.children.insert(1, new_node)
        else:
            current_node.children.insert(0, new_node)

    return result_huffman_tree







huffman_map = {}
with open("../tmp/enwik8_dict_huffman", 'rb') as f:
    huffman_map = pickle.load(f)

huffman_map_words = {}
with open("../tmp/enwik8_dict_words_huffman", 'rb') as f:
    huffman_map_words = pickle.load(f)



huffman_tree_chars = convert_huffman_map_to_tree(huffman_map)
huffman_tree_words = convert_huffman_map_to_tree(huffman_map_words)

huffman_tree = []

root_node:Node = Node("root", 0)
root_node.children.append(huffman_tree_chars[0])
root_node.children.append(huffman_tree_words[0])

huffman_tree.append(root_node)

encode_the_node(huffman_tree[0])

cutoff_in = 0
cutoff = 0
with open("../tmp/enwik8_cutoff", 'rb') as f:
    cutoff_in = pickle.load(f)


output_final = ""
parent_node = huffman_tree[0]
current_node = parent_node
decoded_string = ""

total_count = 469800763
newCount = 0
with open("../tmp/enwik8_output", "w", encoding="utf-8", newline='\n') as f0:
    with open("../tmp/enwik8_compressed", "rb") as f:
        byte = f.read(1)
        while byte != b"":
            # Do stuff with byte.
            newCount = newCount + 1
            if newCount % 100000 == 0:
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
                if character == "1":
                    current_node = current_node.children[1]
                else:
                    current_node = current_node.children[0]

                if len(current_node.children) == 0:
                    output_final = output_final + current_node.character
                    current_node = parent_node
                    if len(output_final) > 8:
                        tmp_output_final = output_final[:8]
                        output_final = output_final[8:]
                        f0.write(tmp_output_final)

        if len(output_final) > 0:
            f0.write(output_final)
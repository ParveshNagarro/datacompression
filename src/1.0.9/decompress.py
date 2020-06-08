import io
import pickle


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

#rare_chars_root = final_dict_of_all_nodes["Rare_characters_aboch8663"]


output_final = "" + first_word
parent_node = final_dict_of_all_nodes[first_word]
current_node = parent_node
decoded_string = ""

pointer = None

total_count = 100000000
newCount = 0
with open("../../data/tmp/enwik8_output", "w", encoding="utf-8", newline='\n') as f0:
    with open("../../data/tmp/enwik8_compressed", "rb") as f:
        byte = f.read(1)
        while byte != b"":
            # Do stuff with byte.
            newCount = newCount + 1
            if newCount % 10000 == 0:
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
                if isinstance(current_node, Node) and isinstance(current_node.children[0], Child):
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

                    if isinstance(current_node, Node):
                        output_final = output_final + current_node.character
                        child_node_with_rare_char = current_node
                        current_node = pointer
                        pointer = child_node_with_rare_char
                    else:
                        current_node = final_dict_of_all_nodes[current_node.node_character]
                        if current_node.is_rare_children_node is True:
                            pointer = current_node
                            current_node = current_node.children_rare[0]
                        else:
                            if pointer is None:
                                if len(first_word) > 1 and len(current_node.character) > 1:
                                    output_final = output_final + " " + current_node.character
                                else :
                                    output_final = output_final + current_node.character

                            elif len(pointer.character) > 1 and len(current_node.character) > 1:
                                output_final = output_final + " " + current_node.character
                            else:
                                output_final = output_final + current_node.character

                            pointer = current_node

                    if len(output_final) > 8:
                        tmp_output_final = output_final[:8]
                        output_final = output_final[8:]
                        f0.write(tmp_output_final)

        if len(output_final) > 0:
            f0.write(output_final)



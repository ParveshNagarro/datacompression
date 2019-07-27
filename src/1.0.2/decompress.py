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


# the program starts here

huffman_tree = []
with open("../../data/tmp/enwik8_dict", 'rb') as f:
    huffman_tree = pickle.load(f)

cutoff_in = 0
cutoff = 0
with open("../../data/tmp/enwik8_cutoff", 'rb') as f:
    cutoff_in = pickle.load(f)


output_final = ""
parent_node = huffman_tree[0]
current_node = parent_node

with open("../../data/tmp/enwik8_output", "w", encoding="utf-8") as f0:
    with open("../../data/tmp/enwik8_compressed", "rb") as f:
        byte = f.read(1)
        while byte != b"":
            # Do stuff with byte.

            byte_temp = byte
            byte = f.read(1)
            print(hex(int.from_bytes(byte_temp, "big")))
            print(byte_temp)
            decoded_string = "{0:b}".format(ord(byte_temp))

            if byte == b"":
                cutoff = 8 - len(decoded_string)
                cutoff = cutoff - cutoff_in
                if cutoff < 0:
                    cutoff = 0
                decoded_string = ("0" * cutoff) + decoded_string
            print(decoded_string)

            for character in decoded_string:
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
                        print(tmp_output_final)
                        f0.write(tmp_output_final)

        if len(output_final) > 0:
            f0.write(output_final)



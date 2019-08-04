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


def append_the_node(huffman_tree_node: Node, nodes_collect:{}):
    if len(huffman_tree_node.children) > 0:
        append_the_node(huffman_tree_node.children[0], nodes_collect)
        if (len(huffman_tree_node.children)) > 1:
            append_the_node(huffman_tree_node.children[1], nodes_collect)
    else:
        nodes_collect[huffman_tree_node.character] = huffman_tree_node

huffman_tree = []
with open("../../data/tmp/enwik8_dict", 'rb') as f:
    huffman_tree = pickle.load(f)


nodes_dict = {}
append_the_node(huffman_tree[0], nodes_dict)


encoded_contents = ""

print("Reading and the conversion is complete, it's time to write the file back.")
enwik_output: str = "../../data/tmp/enwik8_compressed"
print("The compressed version will be written to " + enwik_output)
cutoff = 0

enwik: str = "../../data/tmp/enwik8"
count = 100000000

newCount = 0
print("doing the compression")
with open(enwik_output, "w+b") as fo:
    with open(enwik, "r", encoding="utf-8") as f:
        while True:
            c = f.readline(1)
            newCount = newCount + 1
            if newCount % 10000 == 0:
                print("percentage of file read" + str((newCount * 100) / count))
            if not c:
                print("End of file. writing whatever is left")
                bytes_array = []
                while len(encoded_contents) > 0:
                    if len(encoded_contents) > 8:
                        string_to_write = encoded_contents[:8]
                        encoded_contents = encoded_contents[8:]
                        #print(int(string_to_write, 2))
                        bytes_array.append(int(string_to_write, 2))
                        #print(hex(int(string_to_write, 2)))
                        #print(string_to_write)

                    else:
                        string_to_write = encoded_contents
                        encoded_contents = ""
                        cutoff = 8 - len(string_to_write)
                        bytes_array.append(int(string_to_write, 2))
                        string_to_write = encoded_contents + ("0" * cutoff)
                        #print(int(string_to_write, 2))
                        #print(hex(int(string_to_write, 2)))
                        #print(string_to_write)
                        #print(cutoff)

                fo.write(bytearray(bytes_array))
                #print(bytes_array)

                break
            encoded_contents = encoded_contents + nodes_dict[c].encoded_string
            while len(encoded_contents) > 8:
                bytes_array = []
                string_to_write = encoded_contents[:8]
                encoded_contents = encoded_contents[8:]
                #print(int(string_to_write, 2))
                bytes_array.append(int(string_to_write, 2))
                #print(hex(int(string_to_write, 2)))
                #print(string_to_write)
                fo.write(bytearray(bytes_array))
                #print(bytes_array)

print("cutoff" + str(cutoff))
with open("../../data/tmp/enwik8_cutoff", 'wb') as f:
    # Pickle the 'data' dictionary using the highest protocol available.
    pickle.dump(cutoff, f, pickle.HIGHEST_PROTOCOL)

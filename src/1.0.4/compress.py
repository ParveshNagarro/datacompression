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

huffman_tree = []

root_node:Node = Node("root", 0)
root_node.children.append(huffman_tree_chars[0])
root_node.children.append(huffman_tree_words[0])

huffman_tree.append(root_node)

encode_the_node(huffman_tree[0])

nodes_dict_words = {}
append_the_node(huffman_tree_words[0], nodes_dict_words)

nodes_dict_chars = {}
append_the_node(huffman_tree_chars[0], nodes_dict_chars)

encoded_contents = ""

print("Reading the dicts is complete, it's time to write the file back.")
enwik_output: str = "../../data/tmp/enwik8_compressed"
print("The compressed version will be written to " + enwik_output)
cutoff = 0

enwik: str = "../../data/tmp/enwik8"
count = 100000000

newCount = 0
total_number_of_lines = 1128024
print("doing the compression")
with open(enwik_output, "w+b") as fo:
    with open(enwik, "r", encoding="utf-8") as f:
        while True:
            c = f.readline()
            if newCount % 100 == 0:
                print("Compressing - " + str((newCount * 100) / total_number_of_lines))
            newCount = newCount + 1
            if not c:
                print("End of file. writing whatever is left")
                bytes_array = []
                while len(encoded_contents) > 0:
                    if len(encoded_contents) > 8:
                        string_to_write = encoded_contents[:8]
                        encoded_contents = encoded_contents[8:]
                        bytes_array.append(int(string_to_write, 2))
                    else:
                        string_to_write = encoded_contents
                        encoded_contents = ""
                        cutoff = 8 - len(string_to_write)
                        bytes_array.append(int(string_to_write, 2))
                        string_to_write = encoded_contents + ("0" * cutoff)

                fo.write(bytearray(bytes_array))

                break
            line_words_pos_dict = {}

            for key, value in nodes_dict_words.items():
                cursor = 0
                index:int = c.find(key, cursor)
                while index != -1:
                    if index in line_words_pos_dict.keys():
                        if len(line_words_pos_dict[index].character) < len(value.character):
                            line_words_pos_dict[index] = value
                    else:
                        line_words_pos_dict[index] = value
                    cursor = cursor + len(value.character)
                    index: int = c.find(key, cursor)

            iter_index = 0
            while iter_index < len(c):
                if iter_index in line_words_pos_dict.keys():
                    encoded_contents = encoded_contents + line_words_pos_dict[iter_index].encoded_string

                    iter_index = iter_index + len(line_words_pos_dict[iter_index].character)
                else:
                    encoded_contents = encoded_contents + nodes_dict_chars[c[iter_index]].encoded_string

                    iter_index = iter_index + 1

            #encoded_contents = encoded_contents + nodes_dict_chars['\n'].encoded_string

            while len(encoded_contents) > 8:
                bytes_array = []
                string_to_write = encoded_contents[:8]
                encoded_contents = encoded_contents[8:]
                bytes_array.append(int(string_to_write, 2))
                fo.write(bytearray(bytes_array))

print("cutoff" + str(cutoff))
with open("../../data/tmp/enwik8_cutoff", 'wb') as f:
    # Pickle the 'data' dictionary using the highest protocol available.
    pickle.dump(cutoff, f, pickle.HIGHEST_PROTOCOL)

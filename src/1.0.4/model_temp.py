import io
import pickle
import re

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
    print("Creating a new node with characters " + node1.character + node2.character + "  and string " + str(
        node1.frequency + node2.frequency))
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
    if node.children is not None and 0 < len(node.children):
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
total_number_of_lines = 1128024
enwik: str = "../../data/tmp/enwik8"
print("Reading the file " + enwik)

my_string = ""
str_to_compare  = ""

count = 0
length = 10
word_nodes_dict = {}
charcters_read = 0


with open("../../data/tmp/enwik8_dict_words", 'rb') as f1:
    huffman_tree_words = pickle.load(f1)

with open("../../data/tmp/enwik8_length", 'rb') as f2:
    length = pickle.load(f2)

with open("../../data/tmp/enwik8_characters_read", 'rb') as f3:
    charcters_read = pickle.load(f3)




for length in range(10,101):
    # working for length 1

    while len(my_string) < length;
        line = f.readline()

    length = length + 1

    while True:
        with open(enwik, "r", encoding="utf-8") as f:

            print("Creating a list of words.....")
            while len(my_string) < length:
                line = f.readline(1)
                my_string = my_string + line

            while len(my_string) < charcters_read:
                line = f.readline(1)
                str_to_compare = str_to_compare + line
                str_to_compare = str_to_compare[1:]
            my_string = my_string[-length:]

            charcters_read = charcters_read + 1

            if my_string in word_nodes_dict:
                continue;
            else:
                node = Node(my_string, 1)
                word_nodes_dict[my_string] = node

            str_to_compare = my_string
            while True:
                line = f.readline(1)
                count = count + 1

                if count % 10000 == 0:
                    print("Creating the words dict - " + str((count * 100) / 101128023))
                if not line:
                    print("End of file")
                    break

                str_to_compare = str_to_compare + line
                str_to_compare = str_to_compare[1:]

                if my_string == str_to_compare:
                    if my_string in word_nodes_dict:
                        node: Node = word_nodes_dict[my_string]
                        node.frequency = node.frequency + 1

            print("total number of lines =  " + str(count))


            print("This is the words array.. only putting the words with frequency greater than 1 in the dict")
            final_word_nodes_dict = {}
            for key, value in word_nodes_dict.items():
                if value.frequency > 1:
                    final_word_nodes_dict[key] = value

            print("Converting the final dict into a list of nodes")
            word_nodes_list = []
            for key, value in final_word_nodes_dict.items():
                word_nodes_list.append(value)

            word_nodes_list.sort(key=lambda x: x.frequency, reverse=False)

            print("The entire contents after the sorting and node creations")
            print_a_list(word_nodes_list)

            word_huffman_tree = []
            for value in word_nodes_list:
                word_huffman_tree.append(value)

            print("Iterating and merging the nodes until only one remains")
            while len(word_huffman_tree) > 1:
                huffman_iteration(word_huffman_tree)
            print_a_list(word_huffman_tree)

            encode_the_node(word_huffman_tree[0])
            print_a_list(word_huffman_tree)

            with open("../../data/tmp/enwik8_dict_words", 'wb') as f4:
                # Pickle the 'data' dictionary using the highest protocol available.
                pickle.dump(word_nodes_dict, f4, pickle.HIGHEST_PROTOCOL)

            with open("../../data/tmp/enwik8_length", 'wb') as f5:
                # Pickle the 'data' dictionary using the highest protocol available.
                pickle.dump(length, f5, pickle.HIGHEST_PROTOCOL)

            with open("../../data/tmp/enwik8_characters_read", 'wb') as f6:
                # Pickle the 'data' dictionary using the highest protocol available.
                pickle.dump(charcters_read, f6, pickle.HIGHEST_PROTOCOL)


    charcters_read = 0

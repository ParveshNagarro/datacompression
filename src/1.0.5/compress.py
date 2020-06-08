import io
import pickle
import matplotlib.pyplot as plt
import random

r = random.Random()
r.seed("huffman")

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


# x axis values
x = []
# corresponding y axis values
y = []


y1 = []
correctPredictionsArr = []


enwik_output: str = "../../data/tmp/enwik8_compressed"
print("The compressed version will be written to " + enwik_output)
cutoff = 0

enwik: str = "../../data/tmp/enwik8"
count = 100000000

newCount = 0
xscale  = 1000000

correctPredictions = 0

count0 = 0
count1 = 0

prediction = 1

with open(enwik, "r", encoding="utf-8") as f:
    while True:
        c = f.read(1)
        if newCount % xscale  == 0:
            print("Compressing - " + str((newCount * 100) / count))
            x.append(newCount)
            y.append(count0)
            y1.append(count1)
            correctPredictionsArr.append(correctPredictions)

            if (newCount / 10) % xscale == 0:
                print("count of zeroes is ")
                print(count0)

                print("count of ones is ")
                print(count1)

                print("correct predictions ")
                print(correctPredictions)

                print(x)
                print(y)
                print(y1)

        newCount = newCount + 1
        if not c:
            break
        b = ord(c)
        for i in range(8):
            bit = 2 ** i & b
            if bit > 0:
                if prediction > 0:
                    correctPredictions = correctPredictions + 1
                count1 = count1 + 1
            else:
                if prediction == 0:
                    correctPredictions = correctPredictions + 1
                count0 = count0 + 1

            prediction = prediction + r.randint(1,100)
            prediction = prediction % 2

print("count of zeroes is ")
print(count0)

print("count of ones is ")
print(count1)

print("correct predictions ")
print(correctPredictions)

print(x)
print(y)
print(y1)
print(correctPredictionsArr)

# plotting the points
plt.plot(x, y)
plt.plot(x, y1)

# naming the x axis
plt.xlabel('x - axis')
# naming the y axis
plt.ylabel('y - axis')

# giving a title to my graph
plt.title('My first graph!')

# function to show the plot
plt.show()
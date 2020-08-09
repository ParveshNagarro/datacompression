ENWIK_FILENAME = "../data/enwik9"
NUMBER_OF_LINES =  13147026

class Node:
  def __init__(self, character, frequency):
    self.character = character
    self.frequency = frequency
    self.encoded_string = ""

dict_nodes = {}
count  = 0
with open(ENWIK_FILENAME, encoding="utf8") as f:
  while True:
    c = f.read(1)
    count = count + 1
    if count % 1000000 == 0:
      print("Read " + str(count) + " characters.")
    if not c:
      print("End of file")
      break
    if c in dict_nodes:
      dict_nodes[c].frequency = dict_nodes[c].frequency + 1
    else:
      newNode:Node = Node(c, 1)
      dict_nodes[c] = newNode


print("total characters read : " + str(count))

list_nodes = []
for key, value in dict_nodes.items():
	list_nodes.append(value)

list_nodes.sort(key=lambda x: x.frequency, reverse=True)

with open("../tmp/frequency_distro", "w", encoding="utf8") as f:
  for node in list_nodes:
    f.write(node.character + " - " + str(node.frequency) + "\n")

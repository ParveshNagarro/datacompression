package datacompression;

import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.Currency;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

public class Util {

	static Map<String, String> convertFrequencyMapToHuffmanMap(Map<String, Long> finalWordNodesDict) {
		System.out.println("Converting the final dict into list of nodes.-------" + finalWordNodesDict.size());

		List<Node> wordNodesList = finalWordNodesDict.entrySet().stream().map(e -> new Node(e.getKey(), e.getValue()))
				.collect(Collectors.toList());
		wordNodesList.sort(new NodeComparator());

		List<Node> tmpWordsNodesList = new ArrayList<Node>(wordNodesList);
		wordNodesList.sort(new NodeComparator().reversed());

		List<Node> wordHuffmanTree = new ArrayList<Node>(wordNodesList);

		// System.out.println("Iterating and merging the nodes until only one remains");
		if (wordHuffmanTree.size() > 1) {
			while (wordHuffmanTree.size() > 1) {
				huffmanIteration(wordHuffmanTree);
			}
		} else {
			if (wordHuffmanTree.size() == 1) {
				Node node1 = wordHuffmanTree.get(0);
				wordHuffmanTree.remove(0);
				Node rootNode = new Node("root", 1);
				rootNode.getChildren().add(node1);
				wordHuffmanTree.add(rootNode);
			}
		}

		encodeTheNode(wordHuffmanTree.iterator().next());

		return tmpWordsNodesList.stream().collect(Collectors.toMap(Node::getCharacter, Node::getEncodedString));

	}

	static void encodeTheNode(Node node) {
		// System.out.println("The current node to encode is " + node.getFrequency() +
		// "-" + node.getCharacter());

		if (node.getChildren() != null && node.getChildren().size() > 0) {
			// System.out.println("Now encoding the first child of the node + " +
			// node.getFrequency() + "-" + node.getCharacter());
			node.getChildren().get(0).setEncodedString(node.getEncodedString() + "0");
			encodeTheNode(node.getChildren().get(0));
			if (node.getChildren().size() > 1) {
				// System.out.println("Now encoding the second child of the node + " +
				// node.getFrequency() + "-" + node.getCharacter());
				node.getChildren().get(1).setEncodedString(node.getEncodedString() + "1");
				encodeTheNode(node.getChildren().get(1));
			}
		} else {
			// System.out.println("Nothing to encode in this node as there are either no
			// children");
		}

	}

	static void huffmanIteration(List<Node> huffmanTreeToIterate) {
		System.out.println(
				"Sorting the nodes in the tree. Right now there are " + huffmanTreeToIterate.size() + " nodes.");
		huffmanTreeToIterate.sort(new NodeComparator());
		Node node1 = huffmanTreeToIterate.get(0);
		huffmanTreeToIterate.remove(0);
		Node node2 = huffmanTreeToIterate.get(0);
		huffmanTreeToIterate.remove(0);
		long sum = node1.getFrequency() + node2.getFrequency();
		// System.out.println("Creating a new node with characters " +
		// node1.getCharacter() + node2.getCharacter() + " and string " + sum);

		Node newNode = new Node(node1.getCharacter() + node2.getCharacter(), sum);
		newNode.getChildren().add(node1);
		newNode.getChildren().add(node2);
		huffmanTreeToIterate.add(newNode);

		// System.out.println("Sorting the nodes in the tree. Right now there are " +
		// huffmanTreeToIterate.size() + " nodes.");
		huffmanTreeToIterate.sort(new NodeComparator());
	}

	static void dump(Object object, String filename) {
		try {
			FileOutputStream fileOut = new FileOutputStream(filename);
			ObjectOutputStream out = new ObjectOutputStream(fileOut);
			out.writeObject(object);
			out.close();
			fileOut.close();
			// System.out.printf("Serialized data is saved in " + filename);
		} catch (IOException i) {
			i.printStackTrace();
		}
	}

	static Object load(String filename) {
		try {

			FileInputStream fileIn = new FileInputStream(filename);
			ObjectInputStream objectIn = new ObjectInputStream(fileIn);

			Object obj = objectIn.readObject();

			// System.out.println("The Object has been read from the file");
			objectIn.close();
			return obj;

		} catch (Exception ex) {
			ex.printStackTrace();
			return null;
		}
	}

	static boolean isSpace(String s) {
		return s.trim().length() == 0;
	}

	static void printTimeStamp() {
		DateTimeFormatter dtf = DateTimeFormatter.ofPattern("yyyy/MM/dd HH:mm:ss");
		LocalDateTime now = LocalDateTime.now();
		System.out.println(dtf.format(now));
	}

	static List<Node> convertHuffmanMapToTree(Map<String, String> hufffmanMapInput) {
		final List<Node> resultHuffmanTree = new ArrayList<>();
		
		final Node root = new Node("root", 1);
		resultHuffmanTree.add(root);
		
		
		hufffmanMapInput.entrySet().stream().forEach(entry -> {
			Node currentNode = root;
			char[] chars = entry.getKey().toCharArray();
			for (int i = 0; i < chars.length - 1; i++) {
				String characterHuff = Character.toString(chars[i]);
				
				Node childNodeFound = null;
				for (Node childNodeToCheck : currentNode.getChildren()) {
					if (childNodeToCheck.getCharacterHuff() == characterHuff) {
						childNodeFound = childNodeToCheck;
					}
				}
				
				if (!(childNodeFound == null)) {
					currentNode = childNodeFound;
				} else {
					Node tmpNode = new Node(characterHuff, 1);
					tmpNode.setCharacterHuff(characterHuff);
					if (characterHuff == "1") {
						currentNode.getChildren().add(1, tmpNode);
					} else {
						currentNode.getChildren().add(0, tmpNode);
					}
					currentNode = tmpNode;
				}
				
			}
			
			Node newNode = new Node(entry.getKey(), 1);
			newNode.setEncodedString(entry.getValue());
			String characterHuff = Character.toString(chars[chars.length - 1]);
			newNode.setCharacterHuff(characterHuff);
			
			if (characterHuff == "1") {
				currentNode.getChildren().add(1, newNode);
			} else {
				currentNode.getChildren().add(0, newNode);
			}
		});
		
		return resultHuffmanTree;
	}
}

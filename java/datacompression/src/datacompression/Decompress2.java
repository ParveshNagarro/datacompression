package datacompression;

import static datacompression.Constants.TOTAL_COUNT;
import static datacompression.Util.convertFrequencyMapToHuffmanMap;
import static datacompression.Util.convertHuffmanMapToTree;
import static datacompression.Util.load;

import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStreamWriter;
import java.nio.charset.StandardCharsets;
import java.util.Map;
import java.util.concurrent.TimeUnit;

public class Decompress2 {

	public static void main(String[] args) {
		long startTime = System.nanoTime();

		final Map<String, Node> finalMapCombinedWords = (Map<String, Node>) load(
				"../../tmp/enwik8_new_strucure_encoded_distro_combined_words_1");
		final Map<String, Node> finalMapWords = (Map<String, Node>) load(
				"../../tmp/enwik8_new_strucure_encoded_distro_words_1");
		final Map<String, Node> finalMap = (Map<String, Node>) load("../../tmp/enwik8_new_strucure_encoded_distro_1");

		final Map<String, Map<String, Long>> finalFrequencyMapCombinedWords = (Map<String, Map<String, Long>>) load(
				"../../tmp/enwik8_new_strucure_freq_distro_combined_words");
		final Map<String, Map<String, Long>> finalFrequencyMapWords = (Map<String, Map<String, Long>>) load(
				"../../tmp/enwik8_new_strucure_freq_distro_words");
		final Map<String, Map<String, Long>> finalFrequencyMap = (Map<String, Map<String, Long>>) load(
				"../../tmp/enwik8_new_strucure_freq_distro");

		final Count cutoff = new Count();
		final Count cutoffIn = new Count();
		cutoffIn.count = (int) load("../../tmp/enwik8_cutoff");

		final String firstWord = (String) load("../../tmp/enwik8_first_word");

		final MyString currentWord = new MyString();
		currentWord.string = firstWord;

		final MyString outputFinal = new MyString();
		outputFinal.string = firstWord;

		final MyString lastWordWritten = new MyString();
		lastWordWritten.string = firstWord;

		final MyNodeWrapper currentNode = new MyNodeWrapper();
		final MyString decodedString = new MyString();
		decodedString.string = "";

		final Count c = new Count();

		try (final OutputStreamWriter writer = new OutputStreamWriter(new FileOutputStream("../../tmp/enwik8_output"),
				StandardCharsets.UTF_8); InputStream inputStream = new FileInputStream("../../tmp/enwik8_compressed")) {

			int byteValue = inputStream.read();

			while (byteValue != -1) {
				c.count++;
				if (c.count % 4000 == 0) {
					System.out.println("percentage of file read" + (((double) c.count * 100) / TOTAL_COUNT));
					Util.printTimeStamp();
				}

				int byteTemp = byteValue;
				byteValue = inputStream.read();
				decodedString.string = Integer.toBinaryString(byteTemp);
				String tmpDecodedString = decodedString.string;

				char[] chars = tmpDecodedString.toCharArray();
				for (int i = 0; i < chars.length; i++) {
					String character = Character.toString(chars[i]);

					if (currentNode.node == null) {
						Map<String, Node> mapToUse = finalMap;
						if (currentWord.string.length() > 1) {
							if (finalMapCombinedWords.containsKey(currentWord.string)) {
								mapToUse = finalMapCombinedWords;
							} else {
								mapToUse = finalMapWords;
							}
						}
						currentNode.node = mapToUse.get(currentWord.string);
					}

					while (currentNode.node.children.size() == 1) {
						currentNode.node = currentNode.node.getChildren().iterator().next();
						outputFinal.string = outputFinal.string + currentNode.node.getCharacter();

						Map<String, Node> mapToUse = finalMap;
						Map<String, Map<String, Long>> frequencyMapToUse = finalFrequencyMap;
						if (currentWord.string.length() > 1) {
							if (finalMapCombinedWords.containsKey(currentWord.string)) {
								mapToUse = finalMapCombinedWords;
								frequencyMapToUse = finalFrequencyMapCombinedWords;
							} else {
								mapToUse = finalMapWords;
								frequencyMapToUse = finalFrequencyMapWords;
							}
						}

						frequencyMapToUse.get(currentWord.string).put(currentNode.node.getCharacter(),
								frequencyMapToUse.get(currentWord.string).get(currentNode.node.getCharacter()) - 1);
						if (frequencyMapToUse.get(currentWord.string).get(currentNode.node.getCharacter()) == 0) {
							frequencyMapToUse.get(currentWord.string).remove(currentNode.node.getCharacter());

							if (frequencyMapToUse.get(currentWord.string).size() > 0) {
								if (frequencyMapToUse.get(currentWord.string).size() <= 10) {
									mapToUse.put(
											currentWord.string, Util
													.convertHuffmanMapToTree(Util.convertFrequencyMapToHuffmanMap(
															frequencyMapToUse.get(currentWord.string)))
													.iterator().next());
								}
							} else {
								mapToUse.remove(currentWord.string);
								frequencyMapToUse.remove(currentWord.string);
								System.out.println("fun fun fun ------" + mapToUse.size());
							}
						}

						currentWord.string = currentNode.node.getCharacter();

						mapToUse = finalMap;
						if (currentWord.string.length() > 1) {
							if (finalMapCombinedWords.containsKey(currentWord.string)) {
								mapToUse = finalMapCombinedWords;
							} else {
								mapToUse = finalMapWords;
							}
						}
						currentNode.node = mapToUse.get(currentWord.string);

					}

					if (character == "1") {
						currentNode.node = currentNode.node.getChildren().get(1);
					} else {
						currentNode.node = currentNode.node.getChildren().get(0);
					}

					if (currentNode.node.getChildren().size() == 0) {

						outputFinal.string = outputFinal.string + currentNode.node.getCharacter();

						Map<String, Map<String, Long>> frequencyMapToUse = finalFrequencyMap;
						Map<String, Node> mapToUse = finalMap;
						if (currentWord.string.length() > 1) {
							if (finalMapCombinedWords.containsKey(currentWord.string)) {
								mapToUse = finalMapCombinedWords;
								frequencyMapToUse = finalFrequencyMapCombinedWords;
							} else {
								mapToUse = finalMapWords;
								frequencyMapToUse = finalFrequencyMapWords;
							}
						}

						frequencyMapToUse.get(currentWord.string).put(currentNode.node.getCharacter(),
								frequencyMapToUse.get(currentWord.string).get(currentNode.node.getCharacter()) - 1);
						if (frequencyMapToUse.get(currentWord.string).get(currentNode.node.getCharacter()) == 0) {
							frequencyMapToUse.get(currentWord.string).remove(currentNode.node.getCharacter());

							if (frequencyMapToUse.get(currentWord.string).size() > 0) {
								if (frequencyMapToUse.get(currentWord.string).size() <= 10) {
									mapToUse.put(currentWord.string, convertHuffmanMapToTree(
											convertFrequencyMapToHuffmanMap(frequencyMapToUse.get(currentWord.string)))
													.iterator().next());
								}
							} else {
								mapToUse.remove(currentWord.string);
								frequencyMapToUse.remove(currentWord.string);
								System.out.println("fun fun fun fun-----" + mapToUse.size());
							}
						}

						currentWord.string = currentNode.node.getCharacter();
						currentNode.node = null;

						if (outputFinal.string.length() > 8) {
							writer.write(outputFinal.string.substring(0, 8));
							outputFinal.string = outputFinal.string.substring(8);
						}

					}
				}
			}

			System.out.println("->->->->->->->--the last word-->->-->->->->->");

			if (currentNode.node == null) {
				Map<String, Node> mapToUse = finalMap;
				if (currentWord.string.length() > 1) {
					if (finalMapCombinedWords.containsKey(currentWord.string)) {
						mapToUse = finalMapCombinedWords;
					} else {
						mapToUse = finalMapWords;
					}
				}
				currentNode.node = mapToUse.get(currentWord.string);
			}

			while (currentNode.node != null && currentNode.node.getChildren().size() == 1) {
				currentNode.node = currentNode.node.getChildren().iterator().next();

				if (currentNode.node.getCharacter() == Constants.EOF_CUSTOM) {
					break;
				}

				outputFinal.string = outputFinal.string + currentNode.node.getCharacter();

				Map<String, Node> mapToUse = finalMap;
				Map<String, Map<String, Long>> frequencyMapToUse = finalFrequencyMap;
				if (currentWord.string.length() > 1) {
					if (finalMapCombinedWords.containsKey(currentWord.string)) {
						mapToUse = finalMapCombinedWords;
						frequencyMapToUse = finalFrequencyMapCombinedWords;
					} else {
						mapToUse = finalMapWords;
						frequencyMapToUse = finalFrequencyMapWords;
					}
				}

				frequencyMapToUse.get(currentWord.string).put(currentNode.node.getCharacter(),
						frequencyMapToUse.get(currentWord.string).get(currentNode.node.getCharacter()) - 1);
				if (frequencyMapToUse.get(currentWord.string).get(currentNode.node.getCharacter()) == 0) {
					frequencyMapToUse.get(currentWord.string).remove(currentNode.node.getCharacter());

					if (frequencyMapToUse.get(currentWord.string).size() > 0) {
						if (frequencyMapToUse.get(currentWord.string).size() <= 10) {
							mapToUse.put(currentWord.string,
									convertHuffmanMapToTree(
											convertFrequencyMapToHuffmanMap(frequencyMapToUse.get(currentWord.string)))
													.iterator().next());
						}
					} else {
						mapToUse.remove(currentWord.string);
						frequencyMapToUse.remove(currentWord.string);
						System.out.println("fun fun fun fun-----" + mapToUse.size());
					}
				}

				currentWord.string = currentNode.node.getCharacter();

				mapToUse = finalMap;
				if (currentWord.string.length() > 1) {
					if (finalMapCombinedWords.containsKey(currentWord.string)) {
						mapToUse = finalMapCombinedWords;
					} else {
						mapToUse = finalMapWords;
					}
				}
				currentNode.node = mapToUse.get(currentWord.string);
			}

			if (outputFinal.string.length() > 0) {
				writer.write(outputFinal.string);
			}
		} catch (FileNotFoundException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		}

		long endTime = System.nanoTime();
		long duration = (endTime - startTime);
		System.out.println("time taken " + TimeUnit.SECONDS.convert(duration, TimeUnit.NANOSECONDS));
	}
}

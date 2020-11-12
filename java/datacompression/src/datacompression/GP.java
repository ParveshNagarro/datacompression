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
import java.security.Principal;
import java.util.Collections;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

public class GP {
	public static void main(String[] args) {
		long startTime = System.nanoTime();

		Map<String, String> huffmanMapWords = (Map<String, String>) load("../../tmp/enwik8_dict_words_huffman");
		Map<String, String> huffmanMap = (Map<String, String>) load("../../tmp/enwik8_dict_huffman");

		List<String> collect = huffmanMapWords.keySet().stream().collect(Collectors.toList());
		Collections.sort(collect);
		
		printAList(collect, "words_list");
		
		System.out.println("Reading the dicts is complete, now creating the new structure.");
		collect = huffmanMap.keySet().stream().collect(Collectors.toList());
		Collections.sort(collect);

		printAList(collect, "chars_list");
	}
	static void printAList(List<String> list, String filename) {
		try (final OutputStreamWriter writer = new OutputStreamWriter(new FileOutputStream("../../tmp/" + filename),
				StandardCharsets.UTF_8)) {
			for (String a :list) {
				writer.write(a + "\n");
			}
		} catch (FileNotFoundException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
}

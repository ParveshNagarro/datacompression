package datacompression;

import static datacompression.Constants.ENWIK_FILENAME;
import static datacompression.Constants.MIN_FREQ_TO_BE_A_WORD;
import static datacompression.Constants.NUMBER_OF_LINES;
import static datacompression.Util.convertFrequencyMapToHuffmanMap;
import static datacompression.Util.dump;

import java.io.FileInputStream;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;
import java.util.Map.Entry;
import java.util.concurrent.TimeUnit;
import java.util.stream.Collectors;
import java.util.stream.Stream;

public class Compress1 {

	public static void main(String[] args) {

		long startTime = System.nanoTime();
		
		System.out.println("Here goes nothing++!!!!:)");
		System.out.println("Reading the file " + ENWIK_FILENAME);
		String current = null;
		try {
			current = new java.io.File( "." ).getCanonicalPath();
		} catch (IOException e1) {
			e1.printStackTrace();
		}
        System.out.println("Current dir:"+current);
		final Count c = new Count();
		final Map<String, Long> wordsFrequencyDict = new HashMap<>();
		try (Stream<String> stream = Files.lines(Paths.get(ENWIK_FILENAME))) {
			stream.forEach(line -> {
				c.count++;
				if (c.count % 10000 == 0) {
					float perc = ((float) c.count * 100) / NUMBER_OF_LINES;
					System.out.println("Creating the words dict - " + perc);
				}
				Arrays.asList(line.split("\\W+")).stream().filter(word -> word.length() > 0).forEach(word -> {
					wordsFrequencyDict.put(word,
							wordsFrequencyDict.containsKey(word) ? wordsFrequencyDict.get(word) + 1 : 1L);
				});
			});
		} catch (IOException e) {
			e.printStackTrace();
		}

		System.out
				.println("This is the words array.. only putting the words with frequency greater than 1 in the dict");
		final Map<String, Long> finalWordsFrequencyDict = wordsFrequencyDict.entrySet().stream()
				.filter(e -> e.getValue() >= MIN_FREQ_TO_BE_A_WORD)
				.collect(Collectors.toMap(Entry::getKey, Entry::getValue));

		final Map<String, String> huffmanMapWords = convertFrequencyMapToHuffmanMap(finalWordsFrequencyDict);
		dump(huffmanMapWords, "../../tmp/enwik8_dict_words_huffman");

		System.out.println("creating the characters huffman tree now");

		final Map<String, Long> nodesDict = new HashMap<>();
		
		try {
			FileInputStream fileInput = new FileInputStream(ENWIK_FILENAME);
			System.out.println("The current approach is a little bit better so reading only one character at a time.");
			final Count c1 = new Count();
			int r;
			while ((r = fileInput.read()) != -1) {
				String characterRead = Character.toString((char) r);
				c1.count++;
				if (c1.count % 1000000 == 0) {
					  System.out.println("------" + characterRead + "---" + c1.count);
				}
				
				nodesDict.put(characterRead,
						nodesDict.containsKey(characterRead) ? nodesDict.get(characterRead) + 1 : 1L);
			}
			fileInput.close();
		} catch (Exception e) {
			e.printStackTrace();
		}
		
		System.out.println("Subtracting the frequencies that are being used by the words  ");
		finalWordsFrequencyDict.entrySet().stream().forEach(entry -> {
			char[] chars = entry.getKey().toCharArray();
			for (int i = 0; i < chars.length; i++) {
				String charAtpos = Character.toString(chars[i]);
				nodesDict.put(charAtpos, nodesDict.get(charAtpos) - entry.getValue());
			}
		});
		
		
		System.out.println("This is the characters array.. only putting the words with frequency greater than 0 in the dict");
		Map<String, Long> finalNodesDict =  nodesDict.entrySet().stream()
				.filter(e -> e.getValue() > 0)
				.collect(Collectors.toMap(Entry::getKey, Entry::getValue));
		
		final Map<String, String> huffmanMap = convertFrequencyMapToHuffmanMap(finalNodesDict);
		dump(huffmanMap, "../../tmp/enwik8_dict_huffman");
		
		long endTime = System.nanoTime();

		long duration = (endTime - startTime);
		System.out.println("time taken " + TimeUnit.SECONDS.convert(duration, TimeUnit.NANOSECONDS));
	}
}

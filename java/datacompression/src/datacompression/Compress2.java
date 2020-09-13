package datacompression;

import static datacompression.Constants.DISPLAY_CONTROL;
import static datacompression.Constants.ENWIK_FILENAME;
import static datacompression.Constants.EOF_CUSTOM;
import static datacompression.Constants.MIN_FREQ_TO_BE_A_COMBINED_WORD;
import static datacompression.Constants.NUMBER_OF_LINES;
import static datacompression.Util.dump;
import static datacompression.Util.load;

import java.awt.DisplayMode;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.Arrays;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.Set;
import java.util.concurrent.TimeUnit;
import java.util.stream.Stream;

import org.omg.PortableInterceptor.DISCARDING;

public class Compress2 {
	public static void main(String[] args) {
		
		long startTime = System.nanoTime();
		
		Map<String, String> huffmanMapWords = (Map<String, String>) load("../../tmp/enwik8_dict_words_huffman");
		Map<String, String> huffmanMap = (Map<String, String>) load("../../tmp/enwik8_dict_huffman");
		
		System.out.println("Reading the dicts is complete, now creating the new structure.");
		
		final Map<String, Map<String, Long>> finalMap = new HashMap<>();
		final Map<String, Map<String, Long>> finalMapWords = new HashMap<>();
		
		
		
		final MyString currentWord = new MyString();
		final Count c = new Count();
		try (Stream<String> stream = Files.lines(Paths.get(ENWIK_FILENAME))) {
			stream.forEach(line -> {
				c.count++;
				if (c.count % DISPLAY_CONTROL == 0) {
					float perc = ((float) c.count * 100) / NUMBER_OF_LINES;
					System.out.println("Compressing - " + perc);
					Util.printTimeStamp();
				}
				
				Set<String> lineAllWords = new HashSet<>();
				Arrays.asList(line.split("\\W+")).stream().filter(word -> word.length() > 0).filter(w -> huffmanMapWords.containsKey(w)).forEach(word -> {
						lineAllWords.add(word);
				});
				
				final Map<Integer, String> lineWordsPosDict = new HashMap<>();
				lineAllWords.stream().forEach(key -> {
					int cursor = 0;
					int index = line.indexOf(key, cursor);
					while (index != -1) {
						if (lineWordsPosDict.containsKey(index)) {
							if (lineWordsPosDict.get(index).length() < key.length()) {
								lineWordsPosDict.put(index, key);	
							}
						} else {
							lineWordsPosDict.put(index, key);
						}
						cursor = cursor + key.length();
						index = line.indexOf(key, cursor);
					}
				});
				int iterIndex = 0;
				while (iterIndex < line.length()) {
					String newWord = null;
					if (lineWordsPosDict.containsKey(iterIndex)) {
						newWord = lineWordsPosDict.get(iterIndex);
						iterIndex = iterIndex + newWord.length();
					} else {
						newWord = Character.toString(line.charAt(iterIndex));
						iterIndex++;
					}
					
					if (currentWord.string == null) {
						currentWord.string = newWord;
						Map<String, Map<String, Long>> mapToUse = finalMap;
						if (newWord.length() > 1) {
							mapToUse = finalMapWords;
						}
						if (!mapToUse.containsKey(newWord)) {
							mapToUse.put(newWord, new HashMap<>());
						}
					} else {
						// putting the new word in the parent map
						Map<String, Map<String, Long>> mapToUse = finalMap;
						if (newWord.length() > 1) {
							mapToUse = finalMapWords;
						}
						if (!mapToUse.containsKey(newWord)) {
							mapToUse.put(newWord, new HashMap<>());
						}
						
						// putting the new word as a child of the previous word
						mapToUse = finalMap;
						if (currentWord.string.length() > 1) {
							mapToUse = finalMapWords;
						}
						
						Map<String, Long> followers = mapToUse.get(currentWord.string);
						followers.put(newWord, followers.containsKey(newWord) ? followers.get(newWord) + 1 : 1);
						currentWord.string = newWord;
					}
				}
				
				
			});
		} catch (IOException e) {
			e.printStackTrace();
		}

		Map<String, Map<String, Long>> mapToUse = finalMap;
		if (currentWord.string.length() > 1) {
			mapToUse = finalMapWords;
		}
		mapToUse.get(currentWord.string).put(EOF_CUSTOM, 1L);
		
		dump(finalMap, "../../tmp/enwik8_new_strucure_freq_distro");
		dump(finalMapWords, "../../tmp/enwik8_new_strucure_freq_distro_words");
		
		final Map<String, Map<String, Long>> combinedWords = new HashMap<>();
		finalMapWords.entrySet().stream().forEach(entry -> {
			entry.getValue().entrySet().stream().filter(childEntry -> childEntry.getValue() >= MIN_FREQ_TO_BE_A_COMBINED_WORD).forEach(childEntry -> {
				combinedWords.put(entry.getKey() + childEntry.getKey(), new HashMap<>());
			});
		});
		
		dump(combinedWords, "../../tmp/enwik8_new_strucure_freq_distro_combined_words");
		
		long endTime = System.nanoTime();

		long duration = (endTime - startTime);
		System.out.println("time taken " + TimeUnit.SECONDS.convert(duration, TimeUnit.NANOSECONDS));
	}
}

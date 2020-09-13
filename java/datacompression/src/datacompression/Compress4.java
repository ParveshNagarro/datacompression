package datacompression;

import static datacompression.Constants.DISPLAY_CONTROL;
import static datacompression.Constants.ENWIK_FILENAME;
import static datacompression.Constants.EOF_CUSTOM;
import static datacompression.Constants.MIN_FREQ_TO_BE_A_COMBINED_WORD;
import static datacompression.Constants.NUMBER_OF_LINES;
import static datacompression.Util.convertFrequencyMapToHuffmanMap;
import static datacompression.Util.dump;
import static datacompression.Util.isSpace;
import static datacompression.Util.load;

import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.Arrays;
import java.util.Comparator;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Map.Entry;
import java.util.concurrent.TimeUnit;
import java.util.Set;
import java.util.stream.Collectors;
import java.util.stream.Stream;

public class Compress4 {
	public static void main(String[] args) {
		long startTime = System.nanoTime();
		
		final Map<String, Long> totalUsage = new HashMap<>();
		
		final Map<String, Map<String, Long>> huffmanCombinedWords =  (Map<String, Map<String, Long>>) load("../../tmp/enwik8_new_strucure_freq_distro_combined_words");
		final Map<String, Set<String>> combinedWordsHelper = new HashMap<>();
		final Set<String> spaceSeperatedCombinedWords = new HashSet<>();
		
		huffmanCombinedWords.entrySet().stream().forEach(entry -> {
			final String key = entry.getKey();
			if (isSpace(key)) {
				spaceSeperatedCombinedWords.add(key);
			} else {
				List<String> wordsInLine = Arrays.asList(key.split("\\W+")).stream().filter(word -> word.length() > 0).collect(Collectors.toList());;
				if (wordsInLine.size() == 0) {
					spaceSeperatedCombinedWords.add(key);
				} else {
					wordsInLine.forEach(wordInLine -> {
						if (combinedWordsHelper.containsKey(wordInLine)) {
							combinedWordsHelper.get(wordInLine).add(wordInLine);
						} else {
							Set<String> newSet = new HashSet<>();
							newSet.add(key);
							combinedWordsHelper.put(wordInLine, newSet);
						}
					});
				}
			}
		});
		
		final Map<String, Map<String, Long>> huffmanMapWords =  (Map<String, Map<String, Long>>) load("../../tmp/enwik8_new_strucure_freq_distro_words");
		final Map<String, Map<String, Long>> huffmanMap =  (Map<String, Map<String, Long>>) load("../../tmp/enwik8_new_strucure_freq_distro");
		
		
		System.out.println("Reading the dicts is complete, now creating the new structure.");
		
		final Map<String, Map<String, Long>> finalMap = new HashMap<>();
		final Map<String, Map<String, Long>> finalMapWords = new HashMap<>();
		final Map<String, Map<String, Long>> finalMapCombinedWords = new HashMap<>();
		
		final Count c = new Count();
		final MyString currentWord = new MyString();
		
		try (Stream<String> stream = Files.lines(Paths.get(ENWIK_FILENAME))) {
			stream.forEach(line -> {
				c.count++;
				if (c.count % DISPLAY_CONTROL == 0) {
					float perc = ((float) c.count * 100) / NUMBER_OF_LINES;
					System.out.println("Compressing - " + perc);
					Util.printTimeStamp();
				}
				
				Set<String> lineAllWords = new HashSet<>();
				final List<String> wordsInLine = Arrays.asList(line.split("\\W+")).stream().filter(word -> word.length() > 0).collect(Collectors.toList());;
				wordsInLine.stream().filter(w -> huffmanMapWords.containsKey(w)).forEach(word -> {
						lineAllWords.add(word);
				});
				
				//Map<postition in line, word to use>
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
				
				final Set<String> combinedWordsHelperClient = new HashSet<>();
				wordsInLine.stream().filter(wordInLine -> combinedWordsHelper.containsKey(wordInLine)).forEach(wordInline -> {
					combinedWordsHelper.get(wordInline).stream().forEach(combinedWord -> combinedWordsHelperClient.add(combinedWord));
				});
				combinedWordsHelperClient.addAll(spaceSeperatedCombinedWords);
				
				combinedWordsHelperClient.stream().forEach(key -> {
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
							if (huffmanCombinedWords.containsKey(newWord)) {
								mapToUse = finalMapCombinedWords;
							} else {
								mapToUse = finalMapWords;	
							}
						}
						if (!mapToUse.containsKey(newWord)) {
							mapToUse.put(newWord, new HashMap<>());
						}
					} else {
						// putting the new word in the parent map
						Map<String, Map<String, Long>> mapToUse = finalMap;
						if (newWord.length() > 1) {
							if (huffmanCombinedWords.containsKey(newWord)) {
								mapToUse = finalMapCombinedWords;
							} else {
								mapToUse = finalMapWords;	
							}
						}
						if (!mapToUse.containsKey(newWord)) {
							mapToUse.put(newWord, new HashMap<>());
						}
						
						// putting the new word as a child of the previous word
						mapToUse = finalMap;
						if (currentWord.string.length() > 1) {
							if (huffmanCombinedWords.containsKey(currentWord.string)) {
								mapToUse = finalMapCombinedWords;
							} else {
								mapToUse = finalMapWords;	
							}
						}
						
						Map<String, Long> followers = mapToUse.get(currentWord.string);
						followers.put(newWord, followers.containsKey(newWord) ? followers.get(newWord) + 1 : 1);
						
						
						String key = "\"" + currentWord.string + "-" + newWord + "\"";
						totalUsage.put(key, totalUsage.containsKey(key) ? totalUsage.get(key) + 1 : 1);
						
						currentWord.string = newWord;
					}
				}
				
				
			});
		} catch (IOException e) {
			e.printStackTrace();
		}
		
		Map<String, Map<String, Long>> mapToUse = finalMap;
		if (currentWord.string.length() > 1) {
			if (huffmanCombinedWords.containsKey(currentWord.string)) {
				mapToUse = finalMapCombinedWords;
			} else {
				mapToUse = finalMapWords;	
			}
		}
		mapToUse.get(currentWord.string).put(EOF_CUSTOM, 1L);
		
		dump(finalMap, "../../tmp/enwik8_new_strucure_freq_distro");
		dump(finalMapWords, "../../tmp/enwik8_new_strucure_freq_distro_words");
		dump(finalMapCombinedWords, "../../tmp/enwik8_new_strucure_freq_distro_combined_words");
		
		
		final Map<String, Map<String, String>> finalEncodedMap = new HashMap<>();
		final Map<String, Map<String, String>> finalEncodedMapWords = new HashMap<>();
		final Map<String, Map<String, String>> finalEncodedMapCombinedWords = new HashMap<>();
		
		finalMap.entrySet().stream().filter(entry -> entry.getValue().size() > 0).forEach(entry -> {
			finalEncodedMap.put(entry.getKey(), convertFrequencyMapToHuffmanMap(entry.getValue()));
		});
		finalMapWords.entrySet().stream().filter(entry -> entry.getValue().size() > 0).forEach(entry -> {
			finalEncodedMapWords.put(entry.getKey(), convertFrequencyMapToHuffmanMap(entry.getValue()));
		});
		finalMapCombinedWords.entrySet().stream().filter(entry -> entry.getValue().size() > 0).forEach(entry -> {
			finalEncodedMapCombinedWords.put(entry.getKey(), convertFrequencyMapToHuffmanMap(entry.getValue()));
		});
		
		dump(finalEncodedMap, "../../tmp/enwik8_new_strucure_encoded_distro");
		dump(finalEncodedMapWords, "../../tmp/enwik8_new_strucure_encoded_distro_words");
		dump(finalEncodedMapCombinedWords, "../../tmp/enwik8_new_strucure_encoded_distro_combined_words");

		
		try (final OutputStreamWriter writer =
	             new OutputStreamWriter(new FileOutputStream("../../tmp/enwik8_total_usage"), StandardCharsets.UTF_8))
	{
			List<Entry<String, Long>> totaUsageList = totalUsage.entrySet().stream().collect(Collectors.toList());
			totaUsageList.sort(Comparator.comparing(object -> {
				Entry<String, Long> entry = (Entry<String, Long>) object;
				return entry.getValue();
			}).reversed());
			
			totaUsageList.stream().forEach(entry -> {
				try {
					writer.write(entry.getKey() + "-" + entry.getValue() + "\n");
				} catch (IOException e) {
					e.printStackTrace();
				}
			});
	}
		catch (FileNotFoundException e) {
		e.printStackTrace();
	} catch (IOException e) {
		e.printStackTrace();
	}
		
		
		long endTime = System.nanoTime();
		long duration = (endTime - startTime);
		System.out.println("time taken " + TimeUnit.SECONDS.convert(duration, TimeUnit.NANOSECONDS));
	}
}

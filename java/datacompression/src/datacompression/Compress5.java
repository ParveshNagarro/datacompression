package datacompression;

import static datacompression.Constants.DISPLAY_CONTROL;
import static datacompression.Constants.ENWIK_FILENAME;
import static datacompression.Constants.ENWIK_OUTPUT;
import static datacompression.Constants.NUMBER_OF_LINES;
import static datacompression.Util.convertFrequencyMapToHuffmanMap;
import static datacompression.Util.dump;
import static datacompression.Util.isSpace;
import static datacompression.Util.load;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.OutputStream;
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
import java.util.Set;
import java.util.concurrent.TimeUnit;
import java.util.stream.Collectors;
import java.util.stream.Stream;

public class Compress5 {
	public static void main(String[] args) {
		long startTime = System.nanoTime();

		final Map<String, Long> totalUsage = new HashMap<>();

		final Map<String, Map<String, String>> finalMapCombinedWords = (Map<String, Map<String, String>>) load(
				"../../tmp/enwik8_new_strucure_encoded_distro_combined_words");
		final Map<String, Set<String>> combinedWordsHelper = new HashMap<>();
		final Set<String> spaceSeperatedCombinedWords = new HashSet<>();

		finalMapCombinedWords.entrySet().stream().forEach(entry -> {
			final String key = entry.getKey();
			if (isSpace(key)) {
				spaceSeperatedCombinedWords.add(key);
			} else {
				List<String> wordsInLine = Arrays.asList(key.split("\\W+")).stream().filter(word -> word.length() > 0)
						.collect(Collectors.toList());
				;
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

		final Map<String, Map<String, String>> finalMapWords = (Map<String, Map<String, String>>) load(
				"../../tmp/enwik8_new_strucure_encoded_distro_words");
		final Map<String, Map<String, String>> finalMap = (Map<String, Map<String, String>>) load(
				"../../tmp/enwik8_new_strucure_encoded_distro");

		System.out.println("Reading the dicts is complete, now creating the new structure.");

		final Map<String, Map<String, Long>> finalFrequencyMapCombinedWords = (Map<String, Map<String, Long>>) load(
				"../../tmp/enwik8_new_strucure_freq_distro_combined_words");
		final Map<String, Map<String, Long>> finalFrequencyMapWords = (Map<String, Map<String, Long>>) load(
				"../../tmp/enwik8_new_strucure_freq_distro_words");
		final Map<String, Map<String, Long>> finalFrequencyMap = (Map<String, Map<String, Long>>) load(
				"../../tmp/enwik8_new_strucure_freq_distro");

		final Count c = new Count();
		final MyString currentWord = new MyString();
		final MyString encodedContents = new MyString();
		encodedContents.string = "";
		final MyString firstWord = new MyString();
		final Count cutoff = new Count();

		System.out.println("Doing the compression");
		try (Stream<String> stream = Files.lines(Paths.get(ENWIK_FILENAME));
				OutputStream os = new FileOutputStream(new File(ENWIK_OUTPUT))) {
			stream.forEach(line -> {
				c.count++;
				if (c.count % DISPLAY_CONTROL == 0) {
					float perc = ((float) c.count * 100) / NUMBER_OF_LINES;
					System.out.println("Compressing - " + perc);
					Util.printTimeStamp();
				}

				Set<String> lineAllWords = new HashSet<>();
				final List<String> wordsInLine = Arrays.asList(line.split("\\W+")).stream()
						.filter(word -> word.length() > 0).collect(Collectors.toList());
				;
				wordsInLine.stream().filter(w -> finalMapWords.containsKey(w)).forEach(word -> {
					lineAllWords.add(word);
				});

				// Map<postition in line, word to use>
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
				wordsInLine.stream().filter(wordInLine -> combinedWordsHelper.containsKey(wordInLine))
						.forEach(wordInline -> {
							combinedWordsHelper.get(wordInline).stream()
									.filter(combinedWord -> finalMapCombinedWords.containsKey(combinedWord))
									.forEach(combinedWord -> combinedWordsHelperClient.add(combinedWord));
						});
				combinedWordsHelperClient.addAll(spaceSeperatedCombinedWords.stream()
						.filter(spaceSeparatedWord -> finalMapCombinedWords.containsKey(spaceSeparatedWord))
						.collect(Collectors.toSet()));

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

					if (firstWord.string == null) {
						firstWord.string = newWord;
						currentWord.string = newWord;
					} else {
						Map<String, Map<String, String>> mapToUse = finalMap;
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

						if (mapToUse.get(currentWord.string).size() > 1) {
							encodedContents.string = encodedContents.string
									+ mapToUse.get(currentWord.string).get(newWord);
							String key = "\"" + currentWord.string + "-" + newWord + "\"";
							totalUsage.put(key, totalUsage.containsKey(key) ? totalUsage.get(key) + 1 : 1);
						}

						if (frequencyMapToUse.containsKey(currentWord.string)) {
							if (frequencyMapToUse.get(currentWord.string).containsKey(newWord)) {
								frequencyMapToUse.get(currentWord.string).put(newWord,
										frequencyMapToUse.get(currentWord.string).get(newWord) - 1);
							} else {
								System.out.println("xxxxxxxxx");
							}
						} else {
							System.out.println("wejfkewnfk");
						}

						if (frequencyMapToUse.get(currentWord.string).get(newWord) == 0) {
							mapToUse.get(currentWord.string).remove(newWord);
							frequencyMapToUse.get(currentWord.string).remove(newWord);

							if (frequencyMapToUse.get(currentWord.string).size() > 0) {
								if (frequencyMapToUse.get(currentWord.string).size() <= 10) {
									mapToUse.put(currentWord.string,
											convertFrequencyMapToHuffmanMap(frequencyMapToUse.get(currentWord.string)));
								}
							} else {
								frequencyMapToUse.remove(currentWord.string);
								mapToUse.remove(currentWord.string);

								System.out.println("fun fun fun-----" + mapToUse.size());
							}
						}
						currentWord.string = newWord;
					}
				}

				if (encodedContents.string.length() > 0) {
					int lengthToWrite = encodedContents.string.length();
					byte[] bytesArray = new byte[lengthToWrite % 8 == 0 ? lengthToWrite / 8 : (lengthToWrite / 8) + 1];
					int byteCount = 0;
					while (encodedContents.string.length() > 0) {
						if (encodedContents.string.length() >= 8) {

							encodedContents.string = encodedContents.string.substring(8);
						} else {
							cutoff.count = 8 - encodedContents.string.length();
							bytesArray[byteCount++] = Byte.parseByte(encodedContents.string, 2);
							encodedContents.string = "";
						}
					}

					try {
						os.write(bytesArray);
					} catch (IOException e) {
						e.printStackTrace();
					}
				}

			});

			if (encodedContents.string.length() > 0) {
				int lengthToWrite = encodedContents.string.length();
				byte[] bytesArray = new byte[lengthToWrite % 8 == 0 ? lengthToWrite / 8 : (lengthToWrite / 8) + 1];
				int byteCount = 0;
				while (encodedContents.string.length() > 0) {
					if (encodedContents.string.length() >= 8) {
						bytesArray[byteCount++] = Byte.parseByte(encodedContents.string.substring(0, 8), 2);
						encodedContents.string = encodedContents.string.substring(8);
					} else {
						cutoff.count = 8 - encodedContents.string.length();
						bytesArray[byteCount++] = Byte.parseByte(encodedContents.string, 2);
						encodedContents.string = "";
					}
				}
				os.write(bytesArray);
			}

		} catch (Exception e) {
			e.printStackTrace();
		}

		System.out.println("cutoff---" + cutoff.count);
		dump(cutoff.count, "../../tmp/enwik8_cutoff");
		dump(firstWord.string, "../../tmp/enwik8_first_word");

		try (final OutputStreamWriter writer = new OutputStreamWriter(
				new FileOutputStream("../../tmp/enwik8_total_usage"), StandardCharsets.UTF_8)) {
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

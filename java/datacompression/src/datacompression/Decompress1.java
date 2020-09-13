package datacompression;

import static datacompression.Util.convertHuffmanMapToTree;
import static datacompression.Util.load;

import java.util.HashMap;
import java.util.Map;
import java.util.concurrent.TimeUnit;

public class Decompress1 {
	public static void main(String[] args) {
		long startTime = System.nanoTime();

		final Map<String, Map<String, String>> finalMapCombinedWords =  (Map<String, Map<String, String>>) load("../../tmp/enwik8_new_strucure_encoded_distro_combined_words");
		final Map<String, Map<String, String>> finalMapWords =  (Map<String, Map<String, String>>) load("../../tmp/enwik8_new_strucure_encoded_distro_words");
		final Map<String, Map<String, String>> finalMap =  (Map<String, Map<String, String>>) load("../../tmp/enwik8_new_strucure_encoded_distro");
		
		
		final Map<String, Node> updatedFinalMapCombinedWords = new HashMap<String, Node>();
		final Map<String, Node> updatedFinalMapWords = new HashMap<>();
		final Map<String, Node> updatedFinalMap = new HashMap<>();
		
		finalMapCombinedWords.entrySet().forEach(entry -> {
			System.out.println("1.converting the final map to sub tree of the items" + entry.getKey());
			updatedFinalMapCombinedWords.put(entry.getKey(), convertHuffmanMapToTree(entry.getValue()).iterator().next());
		});

		finalMapWords.entrySet().forEach(entry -> {
			System.out.println("2.converting the final map to sub tree of the items" + entry.getKey());
			updatedFinalMapWords.put(entry.getKey(), Util.convertHuffmanMapToTree(entry.getValue()).iterator().next());
		});

		finalMap.entrySet().forEach(entry -> {
			System.out.println("3.converting the final map to sub tree of the items" + entry.getKey());
			updatedFinalMap.put(entry.getKey(), Util.convertHuffmanMapToTree(entry.getValue()).iterator().next());
		});

		System.out.println("writing first one");
		Util.dump(updatedFinalMapCombinedWords, "../../tmp/enwik8_new_strucure_encoded_distro_combined_words_1");
		
		System.out.println("writing second one");
		Util.dump(updatedFinalMapWords, "../../tmp/enwik8_new_strucure_encoded_distro_words_1");
		
		System.out.println("writing third one");
		Util.dump(updatedFinalMap, "../../tmp/enwik8_new_strucure_encoded_distro_1");
		
		
		long endTime = System.nanoTime();
		long duration = (endTime - startTime);
		System.out.println("time taken " + TimeUnit.SECONDS.convert(duration, TimeUnit.NANOSECONDS));
	}
}

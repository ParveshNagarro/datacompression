package datacompression;

import java.io.FileOutputStream;
import java.io.OutputStreamWriter;
import java.nio.charset.StandardCharsets;
import java.util.HashMap;
import java.util.Map;
import java.util.Map.Entry;

public class AnalysisCompres2 {

	public static void main(String[] args) {
		try (final OutputStreamWriter writer = new OutputStreamWriter(new FileOutputStream("../../tmp/analysis_compress2"),
				StandardCharsets.UTF_8);) {
			
			final Map<String, Map<String, Long>> finalMap = (Map<String, Map<String, Long>>) Util.load("../../tmp/enwik8_new_strucure_freq_distro");
			
			for (Entry<String, Map<String, Long>> entry : finalMap.entrySet()) {
				for (Entry<String, Long> entry1 : entry.getValue().entrySet()) {
					writer.write(entry.getKey() + "-" + entry1.getKey() + "-" + entry1.getValue()+"\n");
				}
			}
			
			
		} catch (Exception e) {
			// TODO: handle exception
		}
		
		try (final OutputStreamWriter writer = new OutputStreamWriter(new FileOutputStream("../../tmp/analysis_compress2_words"),
				StandardCharsets.UTF_8);) {
			
			final Map<String, Map<String, Long>> finalMapWords = (Map<String, Map<String, Long>>) Util.load("../../tmp/enwik8_new_strucure_freq_distro_words");
			
			for (Entry<String, Map<String, Long>> entry : finalMapWords.entrySet()) {
				for (Entry<String, Long> entry1 : entry.getValue().entrySet()) {
					writer.write(entry.getKey() + "-" + entry1.getKey() + "-" + entry1.getValue()+"\n");
				}
			}
			
			
		} catch (Exception e) {
			// TODO: handle exception
		}
		System.out.println("done");
	}
}

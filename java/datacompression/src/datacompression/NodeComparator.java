package datacompression;

import java.util.Comparator;

public class NodeComparator implements Comparator<Node>{

	@Override
	public int compare(Node o1, Node o2) {
		Long result =  o1.getFrequency() - o2.getFrequency();
		if (result == 0) {
			return o1.getCharacter().compareTo(o2.getCharacter());
		}
		return result.intValue();
	}

}

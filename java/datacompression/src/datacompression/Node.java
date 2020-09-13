package datacompression;

import java.util.ArrayList;
import java.util.List;

public class Node {
	String character;
	String encodedString;
	private String characterHuff;
	long frequency;
	List<Node> children;
	
	public Node(String character, long frequency) {
		this.character = character;
		this.frequency = frequency;
		this.encodedString = "";
		this.characterHuff = "";
		this.children = new ArrayList<>();
	}

	public String getCharacter() {
		return character;
	}

	public void setCharacter(String character) {
		this.character = character;
	}

	public String getEncodedString() {
		return encodedString;
	}

	public void setEncodedString(String encodedString) {
		this.encodedString = encodedString;
	}

	public long getFrequency() {
		return frequency;
	}

	public void setFrequency(long frequency) {
		this.frequency = frequency;
	}

	public List<Node> getChildren() {
		return children;
	}

	public void setChildren(List<Node> children) {
		this.children = children;
	}

	public String getCharacterHuff() {
		return characterHuff;
	}

	public void setCharacterHuff(String characterHuff) {
		this.characterHuff = characterHuff;
	}
}

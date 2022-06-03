// I am the sole author of this repository.

import structure5.*;

/**
 * An iterator that yields the consecutive characters of a String, in order
 */
public class CharacterIterator extends AbstractIterator<Character> {
	protected int pos = 0;
	protected String str;

	/* constructs a CharacterIterator for a String
	*@pre: str is not empty
	*@param: str is a String
	*/
	public CharacterIterator(String str) {
		this.str = str;
	}

	/* returns the next character in the String and increments pos
	* @return a Character
	*/
	public Character next() {
		return str.charAt(pos++)
	}

	/* Checks if the String has a next character to iterate over
	* @return a boolean
	*/
	public boolean hasNext() {
		return pos < str.length();
	}

	/* resets position in String to iterate over back to beginning of String
	*
	*/
	public void reset() {
		pos = 0;
	}

	/* gets character at current position in String
	* @return a Character
	*/
	public Character get() {
		return str.charAt(pos);
	}

	/* main method for testing CharacterIterator on Strings
	*
	*/
	public static void main(String[] args) {
		CharacterIterator ci = new CharacterIterator("Hello world!");
   	for (char c : ci) {
      System.out.println(c);
		}
	}
}

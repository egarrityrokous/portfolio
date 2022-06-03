// I am the sole author of this repository.

import structure5.*;
import java.util.Iterator;
import java.util.Scanner;

/**
* Class creates a Trie as a LexiconTrie that holds references to all the words
* in Lexicon by implementing Lexicon and borrowing helper methods from
* LexiconNode.java
*/
public class LexiconTrie implements Lexicon {

    // holds reference to the root node in our LexiconTrie
    private LexiconNode root;

    // keeps track of the count of all of our valid words in our LexiconTrie
    private int count = 0;

    /**
    * A constructor which creates an empty LexiconTrie
    */
    public LexiconTrie() {
      root = new LexiconNode('\0', false);
    }

    /**
    * Adds words to our Lexicon
    * @pre word is not null
    * @post returns boolean representing whether a word was successfully added
    * @return true if word was added to our Lexicon; false otherwise
    */
    public boolean addWord(String word) {
      Assert.pre(!word.equals(null), "Word must not be null.");
      // make sure word is lowercase
      word = word.toLowerCase();
      //we instantiate current LexiconNode as the root
      LexiconNode current = root;
      //iterate through all of the characters in the word
      for (int i = 0; i < word.length(); i++) {
        // set ch to current char in word
        char ch = word.charAt(i);
        // if the current node does not have ch as a child, we add it
        if (current.getChild(ch) == null) {
          current.addChild(new LexiconNode(ch, false));
        }
        // set current to its next child
        current = current.getChild(ch);
      }
      // if current constitutes last char of a word, word was not added to
      // LexiconTrie, so return false
      if (current.isWord) {
        return false;
      }
      // else, current does constitute last char of a word, so set its isWord
      // to true, increment count of words in our LexiconTrie, and return true
      current.isWord = true;
      count++;
      return true;
    }

    /**
    * Adds words to our Lexicon from a valid file
    * @pre filename is a valid file
    * @post int representing number of words added from a valid file is returned
    * @return number of words contained in filename to our Lexicon
    */
    public int addWordsFromFile(String filename) {
      Assert.pre(!filename.equals(null), "Must use a valid filename.");
      int wordCount = 0;
      Scanner sc = new Scanner(new FileStream(filename));
      while (sc.hasNextLine()) {
        String word = sc.nextLine().toLowerCase();
        // add each word, incrementing wordCount only if word is not in trie
        if (addWord(word)) {
          wordCount++;
        }
      }
      sc.close();
      return wordCount;
    }

    /**
    * Removes word from our Lexicon
    * @pre word is not null
    * @post returns boolean representing whether a word was succesfully removed
    * @return true if word is successfully removed from Lexicon; false otherwise
    */
    public boolean removeWord(String word) {
      Assert.pre(!word.equals(null), "Word to be removed must be a valid word.");
      // use helper method to try to find word in our lexicon
      LexiconNode current = findNode(word);
      // if word is not in LexiconTrie, return false
      if (!containsWord(word)) {
        return false;
      }
      // else, current does constitute last char of a word, so set its isWord
      // to false, deincrement word count in our LexiconTrie, and return true
      current.isWord = false;
      count--;
      return true;
    }

    /**
    * Returns the number of words contained in our Lexicon
    * @post returns int representing number of words contained within Lexicon
    * @return an int representing the number of words contained in our Lexicon
    */
    public int numWords() {
      return count;
    }

    /**
    * Returns true if our Lexicon contains word; false otherwise
    * @pre word is not null
    * @post returns boolean representing number whether Lexicon contains a word
    * @return true if our Lexicon contains word, false otherwise
    */
    public boolean containsWord(String word) {
      Assert.pre(!word.equals(null), "Word to be checked must be a valid word.");
      // use helper method to try to find word in our lexicon
      LexiconNode current = findNode(word);
      // if there is no child that constitutes the word we're looking for,
      // return false
      if (current == null) {
        return false;
      // else if current constitutes a word, return true
      } else if (current.isWord) {
        return true;
      }
      // else, return false
      return false;
    }

    /**
    * Returns true if prefix is contained in our Lexicon; false otherwise
    * @pre prefix is not null
    * @post returns boolean representing number whether Lexicon contains prefix
    * @return true if prefix is contained in our Lexicon; false otherwise
    */
    public boolean containsPrefix(String prefix) {
      Assert.pre(!prefix.equals(null), "Prefix to be checked must be a valid prefix.");
      // use helper method to try to find prefix in our lexicon
      LexiconNode current = findNode(prefix);
      // if there is no child that constitutes the prefix we're looking for,
      // return false
      if (current == null) {
        return false;
      }
      // else, return true
      return true;
    }

    /**
    * Returns an iterator for our Lexicon
    * @post returns iteterator for vector of strings of our Lexicon's words
    * @return an iterator for a vector of strings with all words in our Lexicon
    */
    public Iterator<String> iterator() {
      // instantiate iterator for LexiconNodes in our LexiconTrie
      Iterator<LexiconNode> iter = root.iterator();
      // instantiate a lexicon with a size according to the number of words
      // represented by our instance variable count
      Vector<String> lexicon = new Vector<String>(count);

      /* while our iterator still has nodes to iterate over, use below helper
      * method to find all the words in our lexicon by recursively iterating
      * over each next node
      */
      while (iter.hasNext()) {
        findWords("", iter.next(), lexicon);
      }
      return lexicon.iterator();
    }

    /**
    * Helper method for our iterator()
    * @pre LexiconNode provided is not the root
    * @post finds all words in Lexicon by recursively iterator over LexiconTrie
    */
    protected void findWords(String str, LexiconNode current, Vector<String> lexicon) {
      Assert.pre(!current.equals(root), "Provided LexiconNode should not be root.");
      // set our accumulator String to the char constituted by current
      str += current.getChar();
      // add the char at current LexiconNode to our vector of words if current
      // constitutes a word
      if (current.isWord) {
        lexicon.add(str);
      }
      // instantiate an iterator for the LexiconNodes in our LexiconTrie
      Iterator<LexiconNode> iter = current.iterator();
      // while iter still has nodes to iterate over, recurse on next node
      while (iter.hasNext()) {
        findWords(str, iter.next(), lexicon);
      }
    }

    /**
    * Helper method for finding a certain char in the current node
    * @pre word should not be null
    * @post returns LexiconNode ending a certain sequence of chars in a String
    * @return LexiconNode that constitutes the correct char if such node exists;
    * null otherwise
    */
    protected LexiconNode findNode(String str) {
      Assert.pre(!str.equals(null), "Provided word should not be null.");
      str = str.toLowerCase();
      LexiconNode current = root;
      // iterate through all chars in str and set ch to each char in str
      for (int i = 0; i < str.length(); i++) {
        char ch = str.charAt(i);
        // if current node does not have ch as a child, return null
        if (current.getChild(ch) == null) {
          return null;
        }
        // go to next child of current
        current = current.getChild(ch);
      }
      return current;
    }

    /**
    *Optional (extra credit) implementation
    */
    public Set<String> suggestCorrections(String target, int maxDistance) {
      return null;
    }

    /**
    *Optional (extra credit) implementation
    */
    public Set<String> matchRegex(String pattern) {
      return null;
    }

    /**
    * Main method for testing
    */
    public static void main(String[] args) {
      LexiconTrie test = new LexiconTrie();
      test.addWord("news");
      test.addWord("ZEN");
      test.addWord("dot");
      System.out.println(test);
    }
}

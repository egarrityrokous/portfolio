// I am the sole author of this repository.

import structure5.*;
import java.util.Iterator;

/*
* Class builds LexiconNodes, references to letter characters, and ensures that
* LexiconNodes are comparable by implementing Comparatble<LexiconNode>
*/
class LexiconNode implements Comparable<LexiconNode> {

    /* single letter stored in this node */
    protected char letter;

    /* true if this node ends some path that defines a valid word */
    protected boolean isWord;

    /* keeps track of the children of this LexiconNode */
    protected OrderedVector<LexiconNode> children = new OrderedVector<LexiconNode>();

    /**
    * a constructor which creates an empty LexiconNode
    */
    LexiconNode(char letter, boolean isWord) {
      this.letter = letter;
      this.isWord = isWord;
    }

    /**
    * helper method returns the character to which LexiconNode holds a reference
    * @post return the letter referenced by a LexiconNode
    * @return char letter referenced by this
    */
    public char getChar() {
      return letter;
    }

    /**
    * CompareTo method compares one Lexicon Node to another by comparing the
    * the letters they reference
    * @pre o is not null
    * @post difference between the chars of each node is returned
    * @return int that represents this LexiconNode compared to o
    */
    public int compareTo(LexiconNode o) {
      Assert.pre(!(o.equals(null)), "Node must be comparable and not null.");
      return this.letter - o.getChar();
    }

    /**
    * Adds LexiconNode child to correct position in children
    * @pre ln is not null
    * @post a child, LexiconNode ln, is added to children
    */
    public void addChild(LexiconNode ln) {
      Assert.pre(!(ln.equals(null)), "Node must not be null.");
      children.add(ln);
    }

    /**
    * Gets LexiconNode child for 'ch' out of children or returns null otherwise
    * @pre ch is not empty
    * @post child with char ch is returned if it is found or null otherwise
    * @return either ln if the char at ln is equal to ch or null otherwise
    */
    public LexiconNode getChild(char ch) {
      Assert.pre(ch != ' ', "Given character must not be empty.");
      for (LexiconNode ln : children) {
        if (ln.getChar() == ch) {
          return ln;
        }
      }
      return null;
    }

    /**
    * Removes LexiconNode child for 'ch' from children
    * @pre ch is not empty
    * @post child with char ch is removed from children if it is found
    */
    public void removeChild(char ch) {
      Assert.pre(ch != ' ', "Given character must not be empty.");
      for (LexiconNode ln : children) {
        if (ln.getChar() == ch) {
          children.remove(ln);
        }
      }
    }

    /**
    * Creates an Iterator that iterates over children in alphabetical order
    * @pre ch is not empty
    * @post an iterator for children is returned
    * @return an iterator for the children of a LexiconNode
    */
    public Iterator<LexiconNode> iterator() {
      return children.iterator();
    }

    /**
    * Main method for general testing
    */
    public static void main(String[] args) {
      LexiconNode node = new LexiconNode('a', true);
      node.addChild(new LexiconNode('b', false));
      node.addChild(new LexiconNode('c', false));
      node.addChild(new LexiconNode('d', false));
      node.addChild(new LexiconNode('e', false));
      System.out.println(node.getChild('e').getChar());
    }
}

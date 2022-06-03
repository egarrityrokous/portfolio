// I am the sole author of this repository.

import structure5.*;

/**
* SubsetIterator class uses bitwise operations and iterators to calculate all
* possible subsets of a given vector "set" of generic type E.
*/
public class SubsetIterator<E> extends AbstractIterator<Vector<E>> {
  protected long subsetCounter = 0;
  protected long currentSubset = 0;
  protected Vector<E> vec;

  /**
  * Constructs an empty Vector of subsets
  *@pre: vec is an empty Vector
  *@param vec is a Vector of generic type
  */
  public SubsetIterator(Vector<E> vec) {
    this.vec = vec;
    subsetCounter = 1L << vec.size();
  }

  /* returns the current subset represented by the state of subsetCounter and
  * then increments subsetCounter.
	* @return a Vector of generic type E.
	*/
	public Vector<E> next() {
    // current subset is the Vector<E> returned by get() method
    Vector<E> current = get();
    currentSubset++;
    return current;

	}

	/* Checks if currentSubset is a reasonable representation of a subset
	* @return a boolean
	*/
	public boolean hasNext() {
    return currentSubset < subsetCounter;
	}

	/**
	* resets SubsetIterator so that subsetCounter is back at 0.
	*/
	public void reset() {
    subsetCounter = 0;
	}

	/* Gets the correct current subset represented by currentSubset.
	* @return a Vector of generic type E.
	*/
	public Vector<E> get() {
    Vector<E> newVec = new Vector<E>();
    for (int i = 0; i < vec.size(); i++) {
      // adds 1 to i position
      int currentBit = (1 << i);
      // checks if the value of bit i of currentSubset is equal to currentBit
      if ((currentSubset & currentBit) == currentBit) {
        // adds value at bit i to newVec that get() method will return
        newVec.add(vec.get(i));
      }
    }
    return newVec;
	}

	/* main method for testing SubsetIterator on Vectors of generic type E.
	*
	*/
	public static void main(String[] args) {
    Vector<Integer> intVec = new Vector<Integer>();
    // creates a Vector of Integers with numbers from 0 to 7
    for (int j = 0; j < 8; j++) {
      intVec.add(j);
    }

    // creates a SubsetIterator for intVec
    SubsetIterator<Integer> si = new SubsetIterator<Integer>(intVec);
    // keeps track of current subset representation
    int currSubset = 0;
    /* while SubsetIterator has another item to iterate over, print out the
    * current subset
    */
    while(si.hasNext()) {
      System.out.println(si.next());
      currSubset++;
      }
    // print out the current subset representation count
    System.out.println(currSubset);
  }
}

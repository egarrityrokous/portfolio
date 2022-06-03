// I am the sole author of this repository.

/**
 * Helper class for taking diff.
 * Stores two ints
 * This is mostly to be used as a key in the hashtable. */
class IntPair {
	protected int int1;
	protected int int2;

	/** simple constructor
	 * @param in1 value to be assigned to int1
	 * @param in2 value to be assigned to int2 */
	public IntPair(int in1, int in2) {
		int1 = in1;
		int2 = in2;
	}

	/** hashcode:
	 * just adds together the ints.
	 * @return the sum of the hashcodes */
	public int hashCode() {

		// Implements a hash function that adds the stored integers together
		return int1 + int2;
	}


	/** equals method, just compares each int
	 * @param other the Object to be compared to
	 * @pre other is an IntPair
	 * @return whether or not both strings are equal*/
	public boolean equals(Object other) {
		IntPair otherPair = (IntPair) other;
		return otherPair.int1 == int1 && otherPair.int2 == int2;
	}

	/**
	 * toString() method, just concatenates the two ints
	 * @return the concatenation of int1 and int2
	 * */
	public String toString() {
		return int1 + " " + int2;
	}
}

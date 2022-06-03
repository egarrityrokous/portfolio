/**
 * Helper class for taking diff.
 * Stores two ints
 * BetterIntPair has a good hashCode() implementation.
 * This is mostly to be used as a key in the hashtable. */
class BetterIntPair extends IntPair {

	//Constants used in hashing
	private final int hashPrime = 402653189;
	private final int hashMult = 334743597;
	private final int hashAdd = 205380754;

	/** simple constructor
	 * @param in1 value to be assigned to int1
	 * @param in2 value to be assigned to int2 */
	public BetterIntPair(int in1, int in2) {
		super(in1, in2);
	}

	/** hashcode: fast version uses Cater-Wegman universal hashing;
	 * @return the sum of the hashcodes */
	public int hashCode() {
		// implements the improved hashCode() method to obtain improved performance
		return ((hashMult * int1 + hashAdd) % hashPrime)
                + ((hashMult * int2 + hashAdd) % hashPrime);
	}

}

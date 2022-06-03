// I am the sole author of this repository.

/**
* Class to calculate the diff between two files
* */

import structure5.*;
import java.util.Scanner;

/**
* Class to calculate the diff between two files */
public class BetterHashDiff extends Diff {


	// add an instance variable hash table to store previously-calculated diffs
	// this hash table uses BetterIntPair to obtain improved performance
	protected Hashtable<BetterIntPair, Association<Integer, String>> diffTable;

	/**
	* Constructor for diff
	* @param file1Name is the path to the original file
	* @param file2Name is the path to the new version of the file
	*/
	public BetterHashDiff(String file1Name, String file2Name) {
		super(file1Name, file2Name);
		// constructor calls Diff constructor and initializes a hash table
		// using BetterIntPair to obtain improved performance
		diffTable = new Hashtable<BetterIntPair, Association<Integer, String>>();

	}

	/** The recursive helper method for calulating the diff @pre
	 * remainingFile1, remainingFile2, and table are not null @param
	 * remainingFile1Index the first line of file 1 not yet diffed @param
	 * remainingFile2Index the first line of file 2 not yet diffed @return An
	 * association corresponding to the diff between remainingFile1 and
	 * remainingFile2.  The key is the cost of the diff (number of changes
	 * necessary).  The value is the diff output. */
	public Association<Integer, String> diffHelper(int remainingFile1Index, int
			remainingFile2Index) {
		// This iteration of diffHelper uses a hash table with BetterIntPair to
		// obtain better hash performance

		//base case: file1 has no remaining lines
 		if (remainingFile1Index == file1.size()) {
 			return baseCaseHelper(">", remainingFile2Index, file2);
 		}
 		//base case: file2 has no remaining lines
 		if (remainingFile2Index == file2.size()) {
 			return baseCaseHelper("<", remainingFile1Index, file1);
 		}

		// initialize new BetterIntPair with the given file indices
		BetterIntPair betterFileIntPair = new BetterIntPair(remainingFile1Index, remainingFile2Index);

		// if betterFileIntPair is already in diffTable and is not null, return it
		if (diffTable.get(betterFileIntPair) != null) {
			return diffTable.get(betterFileIntPair);
		}
 		//check if first lines match
 		//If so, calculate recursively the optimal result with matching lines
 		//Store that result in an Association in diffTable
 		Association<Integer, String> matchingLines = null;
 		if (file1.get(remainingFile1Index).equals(file2.get(remainingFile2Index))) {
 			matchingLines = diffHelper(remainingFile1Index + 1, remainingFile2Index + 1);
 		}

 		//calculate the cost of removing a line from file1 (store solution in an Association)
 		Association<Integer, String> file1Line;
 		file1Line = diffHelper(remainingFile1Index, remainingFile2Index + 1);

 		//calculate the cost of removing a line from file2 (store solution in an Association)
 		Association<Integer, String> file2Line;
 		file2Line = diffHelper(remainingFile1Index + 1, remainingFile2Index);

		// store a return value in an Association to set and return later
		Association<Integer, String> retVal;
 		//calculate the minimum between the three associations
 		//calculate the return value using the best recursive solution
 		//and return it
 		if (matchingLines != null && matchingLines.getKey() < file1Line.getKey() && matchingLines.getKey() < file2Line.getKey()) {
			retVal = matchingLines;
 		} else if (file1Line.getKey() < file2Line.getKey()) {
 			String value2 = "> " + (remainingFile2Index + 1) + ": " + file2.get(remainingFile2Index) + "\n";
 			value2 += file1Line.getValue();
 			Association<Integer, String> result2 = new Association<Integer, String>(file1Line.getKey() + 1, value2);
			retVal = result2;
 		} else {
 			String value1 = "< " + (remainingFile1Index + 1) + ": " + file1.get(remainingFile1Index) + "\n";
 			value1 += file2Line.getValue();
 			Association<Integer, String> result1 = new Association<Integer, String>(file2Line.getKey() + 1, value1);
			retVal = result1;
		}
		// put the previously-calculated diffs in the diffTable as you recurse
		diffTable.put(betterFileIntPair, retVal);
		// return the originally stored return value
		return retVal;
	}

	/**
	* main method: two command line arguments; the first is the original file,
	* the second is the new version to be compared to. */
	public static void main(String[] args) {
		if (args.length != 2) {
			System.out.println("Usage: java BetterHashDiff <file1> <file2>");
			System.exit(1);
		}
		Diff diff = new BetterHashDiff(args[0], args[1]);
		diff.findDiff();
	}
}

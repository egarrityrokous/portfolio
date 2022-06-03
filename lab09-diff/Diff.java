// I am the sole author of this repository.

/**
 * Class to calculate the diff between two files
 * */

import structure5.*;
import java.util.Scanner;

/**
 * Class to calculate the diff between two files */
public class Diff {

	//original file
	protected Vector<String> file1;
	//new version of the file
	protected Vector<String> file2;

	/**
	 * Constructor for diff
	 * @param file1Name is the path to the original file
	 * @param file2Name is the path to the new version of the file
	 */
	public Diff(String file1Name, String file2Name) {
		file1 = readInFile(file1Name);
		file2 = readInFile(file2Name);
	}

	/**
	 * Reads in the fine given by fileName.
	 * Note that this method requires Java 11.
	 * @param  fileName name of the file
	 * @return each line of the file as elements of a Vector */
	protected Vector<String> readInFile(String fileName) {
		Vector<String> ret = new Vector<String>();
		Scanner sc = new Scanner(new FileStream(fileName));
		while (sc.hasNext()) {
			ret.add(sc.nextLine());
		}
		return ret;
	}

	/**
	 * toString method
	 * @return the concatenation of the two files
	 */
	public String toString() {
		String ret = "-----\nFile 1:\n-----\n";
		for (String line : file1) {
			ret += line + "\n";
		}
		ret += "-----\nFile2:\n-----\n";
		for (String line : file2) {
			ret += line + "\n";
		}
		return ret;
	}

	/**
	 * Finds the diff of two files
	 * @pre 	file1 and file2 are strings holding the
	 * files we want to compare
	 * @post 	the diff is printed to the terminal
	 */
	public void findDiff() {
		System.out.println(diffHelper(0, 0).getValue());
	}

	/**
	* Helper method for diffHelper that returns an Association holding remaining
	* number of differences left and a String containing all of those differences
	* @pre remainingFile1, remainingFile2, and table are not null
	* @param prefix is either < or > depending on fileIndex and filename
	* @param fileIndex is the index of the file Vector we're looking at
	* @param filename holds the lines of the file we want to compare
	* @post Assocation with the # of differences and a String of those differences
	* is returned
	* @return Assocation with Intenger for # of differences and String containing
	* those differences
	*/
	public Association<Integer, String> baseCaseHelper(String prefix, int fileIndex, Vector<String> filename) {
		Association<Integer, String> diffAssoc;
		int count = 0;
		String differences = "";
		for (int i = fileIndex; i < filename.size(); i++) {
			differences += prefix + " " + (i + 1) + ": " + filename.get(i) + "\n";
			count++;
		}
		diffAssoc = new Association<Integer, String>(count, differences);
		return diffAssoc;
	}

	/**
	 * The recursive helper method for calulating the diff
	 * @pre remainingFile1, remainingFile2, and table are not null
	 * @param remainingFile1Index the first line of file 1 not yet diffed
	 * @param remainingFile2Index the first line of file 2 not yet diffed
	 * @post the Association with minimum # of difference calculated is returned
	 * @return An association corresponding to the diff between remainingFile1
	 * and remainingFile2.  The key is the cost of the diff (number of changes
	 * necessary).  The value is the diff output. */
	public Association<Integer, String> diffHelper(int remainingFile1Index, int remainingFile2Index) {

		//base case: file1 has no remaining lines
		if (remainingFile1Index == file1.size()) {
			return baseCaseHelper(">", remainingFile2Index, file2);
		}

		//base case: file2 has no remaining lines
		if (remainingFile2Index == file2.size()) {
			return baseCaseHelper("<", remainingFile1Index, file1);
		}

		//check if first lines match
		//If so, calculate recursively the optimal result with matching lines
		//Store that result in an Association
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

		//calculate the minimum between the three associations
		//calculate the return value using the best recursive solution
		//and return it
		if (matchingLines != null && matchingLines.getKey() < file1Line.getKey() && matchingLines.getKey() < file2Line.getKey()) {
			return matchingLines;
		} else if (file1Line.getKey() < file2Line.getKey()) {
			String value1 = "> " + (remainingFile2Index + 1) + ": " + file2.get(remainingFile2Index) + "\n";
			value1 += file1Line.getValue();
			Association<Integer, String> result1 = new Association<Integer, String>(file1Line.getKey() + 1, value1);
			return result1;
		}
		String value2 = "< " + (remainingFile1Index + 1) + ": " + file1.get(remainingFile1Index) + "\n";
		value2 += file2Line.getValue();
		Association<Integer, String> result2 = new Association<Integer, String>(file2Line.getKey() + 1, value2);
		return result2;
	}

	/**
	 * main method: two command line arguments; the first is the original file,
	 * the second is the new version to be compared to. */
	public static void main(String[] args) {
		if (args.length != 2) {
			System.out.println("Usage: java Diff <file1> <file2>");
			System.exit(1);
		}
		Diff diff = new Diff(args[0], args[1]);
		diff.findDiff();
	}
}

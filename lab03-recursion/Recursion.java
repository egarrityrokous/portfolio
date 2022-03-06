// We are the sole authors of this repository.

/*
 * Recursion.java is a program that solves problems by breaking them down into
 * smaller and smaller subproblems until a base case is reached through a
 * process known as recursion.
 */

import structure5.*;
public class Recursion {

  /***** Warmup 0.1 ********************************************/

  /**
   * Takes a non-negative integer and returns the sum of its digits.
   * @param n a non-negative integer
   * @return the sum of n's digits
   * @pre n should be a non-negative integer
   * @post returns the sum of the digits as a an int
   */
  public static int digitSum(int n) {
    Assert.pre(0 <= n, "n should be a nonnegative integer.");
    // base case if n is zero, the sum of the digits is 0
    if (n == 0) {
      return 0;
    } else {
      // else return the last digit of n and run the method again on the rest
      // of the problem
      return n % 10 + digitSum(n/10);
    }
  }



/**
 * Helper method copyArray; given an array, an int "from" and an int "to" copies the
 *  makes a copy of the array from index from to index to (no inclusive)
 * @param array the array whose elements are to be copied
 * @param from an int indicating the index from where to copy from
 * @param to an int indicating the index at which copying will stop
 * @return the copy of the array from index "from" to index "to"
 * @pre from and to should be within the length of the array but greater than 0; to should be at least as big as from
 * @post the copy of the array from index "from" to index "to"

*/
  public static int [] copyArray(int [] array, int from, int to) {
    int[] newArray = new int [to - from]; // create a new array
    for (int i = from; i < to; i++) { // copy over each element from array to newArray from index "from" to index "to"
      newArray[i - from] = array[i]; // assigning values
    } return newArray; // return newArray
  }

  /***** Warmup 0.2 ********************************************/

  /**
   * Given a set of integers and a target number, determines
   * whethere there is a subset of those numbers that sum to the
   * target number.
   *
   * @param setOfNums a set of numbers that may appear in the subset
   * @param targetSum the target value for the subset
   * @return true if some subset of numbers in setOfNums sums to targetSum
   * @pre set of number should be a set of ints
   * @post return true or false depending on whether some subset of number can add upto the targetSum
*/

  public static boolean canMakeSum(int[] setOfNums, int targetSum) {
    // base case if set of nums is empty, it does not add upto targetSum, so return false
    if (setOfNums.length == 0) {
      return false;
    } else if (setOfNums[0] == targetSum) { // if it adds upto traget sum return true
      return true;
    }
    else {

      //
      boolean include = canMakeSum(copyArray(setOfNums, 1, setOfNums.length), targetSum - setOfNums[0]);
      boolean exclude = canMakeSum(copyArray(setOfNums, 1, setOfNums.length), targetSum);
      return include || exclude;

        }
      }


  /*****  1  ***************************************************/

  /**
   * Return number of cannoballs in pyramid with the given `height`.
   *
   * @param height the height of the cannonball tower
   * @return the number of cannonballs in the entire tower
   * @pre height is non negative Integer
   * @post returns a positive int for the number of cannonballs in the tower
   */
  public static int countCannonballs(int height) {
    Assert.pre(0 <= height, "height should be a positive int.");
    if (height == 0) {
      return 0;
    } else {
      // returns each area, the number of cannonballs on each level of the tower
      // recursively
      return (height * height) + countCannonballs(height - 1);
    }
  }


  /*****  2  ***************************************************/
  /**
   * A method that determines if a string reads the same forwards
   * and backwards.
   *
   * @param str the string to check
   * @return true if `str` is a palindrome.
   * @pre str is a String that should include letters that are all the same case
   * @post returns a boolean true if str is a palindrome, false otherwise
   */
  public static boolean isPalindrome(String str) {
    if (str.length() == 0 || str.length() == 1) {
    return true;
  } else {
    // recursively removes the first and last character of str and compares them
    // until base case is reached
    return str.charAt(0) == str.charAt(str.length() - 1) && isPalindrome(str.substring(1, str.length() - 1));
  }
}

  /*****  3  ***************************************************/

  /**
   * Checks whether `str` is a string of properly nested and matched
   * parens, brackets, and braces.
   *
   * @param str a string of parens, brackets, and braces
   * @return true if str is properly nested and matched
   * @pre str is a String of brackets, braces, or parentheses
   * @post returns true if str is "balanced"
   */
  public static boolean isBalanced(String str) {
    if (str.length() == 0) {
      return true;
    }
    // if str contains at least one balanced set of brackets, parantheses, or
    // braces, remove them and check the next remaining strings
      else if (str.contains("[]")) {
        int bracketIndex = str.indexOf("[]");
        return isBalanced(str.substring(0, bracketIndex) + str.substring(bracketIndex + 2, str.length()));
      }
      else if (str.contains("()")) {
        int bracketIndex = str.indexOf("()");
        return isBalanced(str.substring(0, bracketIndex) + str.substring(bracketIndex + 2, str.length()));
      }
      else if (str.contains("{}")) {
        int bracketIndex = str.indexOf("{}");
        return isBalanced(str.substring(0, bracketIndex) + str.substring(bracketIndex + 2, str.length()));
      }
      else {
    return false;
  } }

  /*****  4  ***************************************************/

  /**
   * A method to print all subsequences of str (order does not matter).
   *
   * @param str string to print all subsequences of
   * @pre str is a String
   * @post prints all possible subsets of str
   */
  public static void subsequences(String str) {
    subsequenceHelper(str, "");
}
  /**
   * Helper method for subsequences method
   * `soFar` keeps track of the characters currently in the substring
   *   being built
   * @param str string to print all subsequences of
   * @param soFar all subsequences of str to be printed
   * @pre str is a String of any length and soFar is an empty string initially
   * @post prints out soFar once it's filled with all subsets of str
   */
  protected static void subsequenceHelper(String str, String soFar) {
    if (str.length() == 0) {
      System.out.print(soFar);
      System.out.print(",");
    }
    else {
      // recursively includes all subsets of first character in str, then the
      // second character, and so on
      subsequenceHelper(str.substring(1, str.length()), soFar + String.valueOf(str.charAt(0)));
      subsequenceHelper(str.substring(1, str.length()), soFar);
    }
  }

  /*****  5  ***************************************************/

  /**
   * A method to print the binary digits of a number.
   *
   * @param number the number to print in binary
   * @pre number should be a positive int
   * @post prints out number in binary form
   */
  public static void printInBinary(int number) {
    Assert.pre(0 <= number, "number should be a positive int.");
    if (number == 0) {
       System.out.print(0);
    } else {
      // divides number by 2 until reaching 0
      printInBinary(number / 2);
      // recursively prints the binary digits on the way back
      System.out.print(String.valueOf(number %2));
    }
  }


  /*****  6a  ***************************************************/


  /**
   * Return whether a subset of the numbers in nums add up to sum,
   * and print them out.
   *
   * @param nums is an array of ints
   * @param targetSum is an int
   * @return a boolean true if a subset of nums can add up to targetsum, false
   * otherwise
   * @pre nums should be an array of ints; targetsum should be an int
   * @post returns a boolean if targetsum is reached, false otherwise, and
   * prints the first true subset it finds
   */

  public static boolean printSubsetSum(int[] nums, int targetSum) {
    if (targetSum == 0){
      return true;
    } else if (nums.length == 0) {
      return false;
      // if subset of nums adds up to targetsum, return true and print it out
    } else if (printSubsetSum(copyArray(nums,1,nums.length), targetSum - nums[0])) {
      System.out.println(nums[0]);
      return true;
    } else if (printSubsetSum(copyArray(nums,1,nums.length), targetSum)) {
      return true;
    } else {
      return false;
    }
  }

  /*****  6b  ***************************************************/

  /**
   * Return the number of different ways elements in nums can be
   * added together to equal sum (you do not need to print them all).
   *
   * @param nums is an array of ints
   * @param targetSum is an int
   * @return a positive int for the number of true subsets found or 0 if
   * none found
   * @pre nums should be an array of ints; targetsum should be an int
   * @post returns a positive int for the number of true subsets found or 0 if
   * none found
   */

  public static int countSubsetSumSolutions(int[] nums, int targetSum) {
    if (nums.length == 0) {
      return 0;
    } else if (nums[0] == targetSum) {
      return 1;
    }
    // counts the number of true recursive calls
    else {
       return countSubsetSumSolutions(copyArray(nums, 1, nums.length), targetSum - nums[0])
        + countSubsetSumSolutions(copyArray(nums, 1, nums.length), targetSum);
     }
  }


  /***********************************************************/

  /**
   * Add testing code to main to demonstrate that each of your
   * recursive methods works properly.
   *
   * Think about the so-called corner cases!
   *
   * Remember the informal contract we are making: as long as all
   * predconditions are met, a method should return with all
   * postconditions met.
   */

  protected static void testCannonballs() {
    System.out.println("Testing cannonballs: ....");
    System.out.println(countCannonballs(3));
    System.out.println(countCannonballs(10));
  }

  protected static void testPalindrome() {
    System.out.println("Testing isPalindrome: ....");
    System.out.println(isPalindrome("mom"));
    System.out.println(isPalindrome("deeded"));
    System.out.println(isPalindrome("ablewasIereIsawelba"));
  }

  protected static void testBalanced() {
    System.out.println("Testing isBalanced: ....");
    System.out.println(isBalanced("[{[()()]}]"));
    System.out.println(isBalanced("[{[()()]}][{[()()]}]"));
    System.out.println(isBalanced("[{[()()]}{]{[()()]}]"));
  }

  protected static void testSubsequence() {
    System.out.println("Testing subsequences: ....");
    subsequences("ABCD");
    System.out.println();
    subsequences("CSCI136");
    System.out.println();
    subsequences("a");
    System.out.println();
    subsequences("");
    System.out.println();
  }

  protected static void testBinary() {
    System.out.println("Testing printInBinary: ....");
    printInBinary(0);
    System.out.println();
    printInBinary(30);
    System.out.println();
    printInBinary(1);
    System.out.println();
    printInBinary(110);
    System.out.println();
    printInBinary(2048);
    System.out.println();
    printInBinary(43);
    System.out.println();
      }

  protected static void testCanMakeSum() {
    System.out.println("Testing canMakeSum: ....");
    int[] numSet = {2, 5, 7, 12, 16, 21, 30};
    System.out.println(canMakeSum(numSet, 21));
    int[] nums = { 3, 7, 1, 8, -3 };
    System.out.println(canMakeSum(nums, 4));
    System.out.println(canMakeSum(nums, 0));
    System.out.println(canMakeSum(nums, 20));
    System.out.println(canMakeSum(nums, 1));
    System.out.println(canMakeSum(numSet, 22));
    System.out.println(canMakeSum(numSet, 3));
    System.out.println(canMakeSum(numSet, 30));
  }

  protected static void testPrintSubsetSum() {
    System.out.println("Testing printSubsetSum: ....");
    int[] numSet = {2, 5, 7, 12, 16, 21, 30};
    printSubsetSum(numSet, 21);
    }
  /*  printSubsetSum(numSet, 22);
    printSubsetSum(numSet, 3);
    printSubsetSum(numSet, 30)
*/
  protected static void testCountSubsetSum() {
    System.out.println("Testing countSubsetSumSolutions: ....");
    int[] numSet = {2, 5, 7, 12, 16, 21, 30};
    System.out.println(countSubsetSumSolutions(numSet, 21));
    System.out.println(countSubsetSumSolutions(numSet, 22));
    System.out.println(countSubsetSumSolutions(numSet, 3));
    System.out.println(countSubsetSumSolutions(numSet, 30));
  }

  /**
   * Main method that calls testing methods to verify
   * the functionality of each lab exercise.
   *
   * Please supplement the testing code with additional
   * correctness tests as needed.
   */
  public static void main(String[] args) {
    testCannonballs();
    testPalindrome();
    testBalanced();
    testSubsequence();
    testBinary();
    testCanMakeSum();
    testPrintSubsetSum();
    testCountSubsetSum();
  }
}

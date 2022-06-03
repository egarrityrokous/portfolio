// I am the sole author of this repository.

import structure5.*;
import static java.lang.Math.*;

/**
* A class implemented to solve the TwoTowers problem from lab07.
*/
public class TwoTowers {

  /**
   * Initializes the block numbers from 1 to n
   * @param an integer
   * @pre n is non-negative
   * @return a vector of Doubles, which represent the block numbers
   */
  protected static Vector<Double> buildVec(int n) {
    Assert.pre(n >= 0, "n must not be negative");
    Vector<Double> vec = new Vector<Double>();
    for (Double i = 1.0; i <= n; i++) {
      vec.add(i);
    }
    return vec;
  }

  /**
   * Returns number of each block in a subset of vec
   * @param vector of Doubles
   * @pre vec is not null
   * @return a vector of integers, which represent the block numbers
   */
  protected static Vector<Integer> blockNumsVec(Vector<Double> vec) {
    Assert.pre(vec != null, "Vector must not be empty.");
    Vector<Integer> blockNumsVec = new Vector<Integer>();
    for (int i = 0; i < vec.size(); i++) {
      blockNumsVec.add((int)Math.round(vec.get(i) * vec.get(i)));
    }
    return blockNumsVec;
  }

  /**
   * Sums the square-rooted heights in vec
   * @param vector of Doubles
   * @pre vec is not null
   * @return a Double, the sum of all the square-rooted heights in vec
   */
  protected static Double findSum(Vector<Double> vec) {
    Assert.pre(vec != null, "Vector must not be empty.");
    Double sum = 0.0;
    for (int i = 0; i < vec.size(); i++) {
      sum += vec.get(i);
    }
    return sum;
  }

  /**
   * Returns the square-rooted heights of each block in a subset of vec
   * @param vector of Double
   * @pre vec is not null
   * @return a vector of Doubles, which represent the square-rooted heights of
   * each block in a subset of vec
   */
  protected static Vector<Double> heightsVec(Vector<Double> vec) {
    Assert.pre(vec != null, "Vector must be non-empty.");
    Vector<Double> heightsVec = new Vector<Double>();
    for (int i = 0; i < vec.size(); i++) {
      heightsVec.add(sqrt(vec.get(i)));
    }
    return heightsVec;
  }

  /**
   * Finds the TwoTowers, the vector subsets, with square-rooted heights closest
   * to the given target
   * @param subsets, a SubsetIterator of vectors of Doubles
   * @param target, a Double
   * @pre subsets is not null; target is not negative
   * @return topTwo, a vector containing two vectors of Doubles
   */
  protected static Vector<Vector<Double>> findTwoTowers(SubsetIterator<Double> subsets, Double target) {
    Assert.pre(subsets != null, "Vector must not be empty.");
    Assert.pre(target >= 0, "Target must be greater than or equal to 0.");
    Double maxSum = 0.0;
    Vector<Double> best = new Vector<Double>();
    Vector<Double> nextBest = new Vector<Double>();

    // iterate through each subset
    while (subsets.hasNext()) {
      // create vec containing square-rooted heights of blocks in next subset
      Vector<Double> heightsVec = heightsVec(subsets.next());
      // find the sum of the heights in heightsVec
      Double current = findSum(heightsVec);
      //find best and nextBest that're closest to target and greater than maxSum
      if ((current <= target) && (current >= maxSum)) {
        // store second closest tower subset as last closest subset tower found
        nextBest = best;
        // update closest tower subset as it's found
        best = heightsVec;
        // update maxSum so that it's the current closest sum to target
        maxSum = current;
        // update nextBest if it's no longer second closest to maxSum
      } else if ((current <= target) && current >= findSum(nextBest)) {
        nextBest = heightsVec;
      }
    }
    // create Vector of two best Vectors found with closest heights to target
    Vector<Vector<Double>> twoBest = new Vector<Vector<Double>>();
    twoBest.add(best);
    twoBest.add(nextBest);
    return twoBest;
  }

  /**
   * Main method for general testing, which prints two best tower solutions for
   * any given block number n, so long as n >= 0
   */
  public static void main(String[] args) {
    int n = Integer.parseInt(args[0]);
    // ensure that n is greater than or equal to 0
    if (n < 0) {
      System.out.println("Block number must be greater than or equal to 0.");
    } else {
      // find subsets for n blocks
      SubsetIterator<Double> vec = new SubsetIterator<Double>(buildVec(n));
      // find answers using findTwoTowers helper method
      Vector<Vector<Double>> twoTowers = findTwoTowers(vec, (findSum(heightsVec(buildVec(n))) / 2));
      // print statements to answer the questions asked by lab07
      System.out.println("There are " + n + " total blocks.");
      System.out.println("Half height (h/2) is: " + (findSum(heightsVec(buildVec(n))) / 2));
      System.out.println("The best subset is: " + blockNumsVec(twoTowers.getFirst()) + " = " + findSum(twoTowers.getFirst()));
      System.out.println("The second best subset is: " + blockNumsVec(twoTowers.getLast()) + " = " + findSum(twoTowers.getLast()));
    }
  }
}

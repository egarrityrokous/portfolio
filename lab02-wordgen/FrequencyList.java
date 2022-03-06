// I am the sole author of this repository.
/* This class creates a frequency list, a vector of associations, that stores
* a set of characters, each of which has an associated integer frequency.
* This class also allows characters to be added to the frequency list, returns
* characters according to their frequency, and prints a string representation
* of the frequency list.
*/

import structure5.*;
import java.util.Random;

/**
* A FrequencyList stores a set of characters each of which has
* an associated integer frequency
*/

public class FrequencyList {
  // FrequencyList is a vector of associations
  protected Vector<Association<String, Integer>> freqList;
  protected int totalFreq = 0;
  protected Random rand = new Random();

  /** Construct an empty FrequencyList */
  public FrequencyList() {
    freqList = new Vector<Association<String, Integer>>();
  }

  /** add(String ch)
  * If ch is in the FrequencyList, increment its associated frequency
  * Otherwise add ch to FrequencyList with frequency 1
  * @param ch is the String to add to the FrequencyList
  */
  public void add(String ch) {
    // initialize ch association for a new association, chAssoc
    Association<String, Integer> chAssoc;
    chAssoc = new Association<String, Integer> (ch, 1);
    int assocIndex = freqList.indexOf(chAssoc);

    // if ch is already in freqList, increment its value by 1
    if (assocIndex != -1) {
      chAssoc = freqList.get(assocIndex);
      chAssoc.setValue(chAssoc.getValue() + 1);
    } else {
      // else, add new association, chAssoc, to freqList
      freqList.add(chAssoc);
      // update total frequency count in freqList
    }
    totalFreq++;
  }

  /** Selects a character from this FrequencyList
  * @return a character from the FrequencyList with probabality equal to its relative frequency
  */
  public char choose() {
    int relFreq = 0;
    // selects random integer from total frequencies of characters in freqList
    int randFreq = rand.nextInt(totalFreq) + 1;

    // iterates through each association in freqList
    for (int i = 0; i < freqList.size(); i++) {
      relFreq += freqList.get(i).getValue();
      /*returns a random character once its frequency probability is equal
      * to its relative frequency
      */
      if (relFreq >= randFreq) {
        return freqList.get(i).getKey().charAt(0);
      }
    }
    return '\0';
  }

  /** Produce a string representation of the FrequencyList
   * @return a String representing the FrequencyList
   */
  public String toString() {
    String result = "";
    for (int i = 0; i < freqList.size(); i++) {
      result += " " + freqList.get(i).getKey() + " appears "
        + freqList.get(i).getValue() + " times.";
    }
    return result;
  }

  // Use main to test your FrequencyList class
  public static void main(String[] args) {
    FrequencyList test = new FrequencyList();
    test.add("Santana");
    System.out.println(test);
  }
}

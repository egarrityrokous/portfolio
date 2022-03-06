// I am the sole author of this repository.

/* The Table class holds a collection of Strings, each of which has an
* associat4ed FrequencyList, and can add FrequencyLists as well as return
* Strings from it with probability equal to their relative frequency.
*/
import structure5.*;

/**
* A Table holds a collection of strings, each of which has an
* associated FrequencyList
*/
public class Table {
  // a Table is a vector of associations
  protected Vector<Association<String, FrequencyList>> table;
  // initialize key association for later use
  protected Association<String, FrequencyList> keyAssoc;


  /** Construct an empty table */
  public Table() {
    table = new Vector<Association<String, FrequencyList>>();
  }

  /**
  * Updates the table as follows
  * If key already exists in the table, update its FrequencyList
  * by adding value to it
  * Otherwise, create a FrequencyList for key and add value to it
  * @param key is the desired k-letter sequence
  * @param value is the character to add to the FrequencyList of key
  */
  public void add(String key, char value) {
    // establish key association
    keyAssoc = new Association<String, FrequencyList>(key, null);
    // initialize keyAssoc index
    int assocIndex = table.indexOf(keyAssoc);

    // checks if keyAssoc is in table; if so, adds value to its FrequencyList
    if (assocIndex != -1) {
      table.get(assocIndex).getValue().add(String.valueOf(value));
    // else, creates a FrequencyLsit for its key and then add value to it
    } else {
      FrequencyList freqList = new FrequencyList();
      freqList.add(String.valueOf(value));
      table.add(new Association<String, FrequencyList>(key, freqList));
    }
  }

  /**
  * If key is in the table, return one of the characters from
  * its FrequencyList with probability equal to its relative frequency
  * Otherwise, determine a reasonable value to return
  * @param key is the k-letter sequence whose frequencies we want to use
  * @return a character selected from the corresponding FrequencyList
  */
  public char choose(String key) {
    // establish key association
    keyAssoc = new Association<String, FrequencyList>(key, null);
    // initialize keyAssoc index
    int assocIndex = table.indexOf(keyAssoc);

    /* checks if keyAssoc is in table; if so, returns one of its characters
    * with probability equal to its relative frequency
    */
    if (assocIndex != -1) {
      FrequencyList freqList = table.get(assocIndex).getValue();
      return freqList.choose();
    }
    // else, returns null character
    return '\0';
  }

  /** Produce a string representation of the Table
  * @return a String representing this Table
  */
  public String toString() {
    String result = "";
    for (int i = 0; i < table.size(); i++) {
      result += "Letters: " + table.get(i).getKey() + ", FrequencyLists: "
        + table.get(i).getValue();
    }
    return result;
  }

  // Use main to test your Table class
  public static void main(String[] args) {
    Table test = new Table();
    test.add("Santana", 'a');
    test.add("Santana", 'x');
    System.out.println(test);
  }
}

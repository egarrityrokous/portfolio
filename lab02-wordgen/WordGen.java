// I am the sole author of this repository.
/* This program reads text files as input and generates new text using the
* frequencies in the Table class.
*/

import structure5.*;
import java.util.Scanner;
import java.util.Random;

/* WordGen class generates new text based on the probabilities of characters
* appearing in input text according their relative frequencies, found in the
* Table class.
*/
public class WordGen {

  // This helper method scans text as input for later use.
  public String scanText() {
    Scanner in = new Scanner(System.in);
    StringBuffer textBuffer = new StringBuffer();
    while (in.hasNextLine()) {
      String line = in.nextLine();
      textBuffer.append(line);
      textBuffer.append("\n");
    }
    String text = textBuffer.toString();
    // 'text' now contains the full contents of the input.
    return text;
  }

  /* This helper method generates a Table of the associations of k-length
  * Strings and the characters following those k-length Strings by using the
  * Table .add() method.
  */
  public void generateTable(String text, int k, Table table) {
    for (int i = 0; i < text.length() - k; i++) {
      String key = text.substring(i, i + k); // k-length String
      char value = text.charAt(i + k); // character after k-length String
      // adds associations of k-length Strings and char following them to table
      table.add(key, value);
    }
  }

  /* This helper method generates random text based on the frequencies of the
  * characters that come after k-length Strings.
  */
  public String generateText(String text, int k, Table table) {
    String result = text.substring(0, k); // gets first k-length String

    for (int i = 0; i < text.length() - k; i++) {
      // generates keys of k-length Strings
      String key = result.substring(i, i + k);
      // chooses random character based with probability equal to its relFreq
      char randChar = table.choose(key);
      // if randChar is null character, we will start over at beginning of text
      if (randChar == '\0') {
        char nonNullRandChar = table.choose(text.substring(0, k));
        result += nonNullRandChar;
      }
      result += randChar;
    }
    return result;
  }

  // main method runs text and generates the random text based from input text
  public static void main(String[] args) {
    if (args.length == 0) {
        // no args, so print usage line and do nothing else
        System.out.println("Usage: java WordGen ");
    } else {
        // convert first argument to k
        int k = Integer.parseInt(args[0]);
        Table table = new Table();
        WordGen randomText = new WordGen();
        String inputText = randomText.scanText();
        randomText.generateTable(inputText, k, table);
        String randomStory = randomText.generateText(inputText, k, table);
        System.out.println(randomStory);
    }
  }
}

// I am the sole author of this repository.

import structure5.*;
import java.util.Comparator;
import java.util.Scanner;

/** Problems.java is a program that runs a main method, which executes
* all necessary functionality to answer the 5 required lab questions on the
* sample student phone book provided.
*/
public class Problems {

  /*
  * Method helps add or increment Associations of where keys are given String.
  * @param vec is given (empty) Vector of Associations of Strings and Integers.
  * @param str is a given String that will be used to create new or increment
  * existing Associations.
	* @post increments or adds Associations where keys are given String.
	*/
  public static void assocHelper(Vector<Association<String, Integer>> vec, String str) {
    if (!str.contains("UNKNOWN") && str != "-1") {
      Association<String, Integer> assoc = new Association<String, Integer> (str, 1);
      // create integer value for index of address association in addressVector
      int assocIndex = vec.indexOf(assoc);
      // if address is already in addressVector, increment its value by 1
      if (assocIndex != -1) {
        assoc = vec.get(assocIndex);
        assoc.setValue(assoc.getValue() + 1);
      } else {
        // else, add new association, addressAssoc, to addressVector
        vec.add(assoc);
      }
    }
  }

  // Main method provides all necessary functionality to answer lab questions.
  public static void main(String[] args) {

    // create new scanner
    Scanner sc = new Scanner(System.in);

    // instantiate the necessary comparators
    StudentNameComparator nameComp = new StudentNameComparator();
    StudentSuBoxComparator suBoxComp = new StudentSuBoxComparator();
    StudentVowelComparator vowelComp = new StudentVowelComparator();
    StudentAddressComparator addressComp = new StudentAddressComparator();
    StudentAreaCodeComparator areaCodeComp = new StudentAreaCodeComparator();

    // create a MyVector example vector of Students
    MyVector<Student> studentVector = new MyVector<Student>();

    /** create a MyVector of associations for each address (key) paired with the
    * number of Students who live there (value).
    */
    MyVector<Association<String, Integer>> addressVector = new MyVector<Association<String, Integer>>();

    /** create a MyVector of associations for each area code (key) paired with
    * the number of Students who have that area code in their home phone number.
    */
    MyVector<Association<String, Integer>> areaCodeVector = new MyVector<Association<String, Integer>>();

    /** While the scanner has a next line, for every three lines, the correct
    * attributes are assigned to each Student in studentVector, skipping every
    * fourth line, since the example phone books provided have a line of '-' for
    * every fourth line.
    */
    while (sc.hasNextLine()) {
      Student s1 = new Student(sc.nextLine(), sc.nextLine(), sc.nextLong(),
        sc.nextInt(), sc.nextLong());
      studentVector.add(s1);
      sc.nextLine();
      sc.nextLine();
    }

    // sort studentVector using insertion sort and the name comparator
    studentVector.insertionSortComparator(nameComp);
    // print out the answer to the first question
    System.out.println("1. " + studentVector.firstElement().getName());

    // sort studentVector using insertion sort and the SU box comparator
    studentVector.insertionSortComparator(suBoxComp);
    // print out the answer to the second question
    System.out.println("2. Smallest: " + studentVector.firstElement().getName()
      + ", " + studentVector.firstElement().getSuBox() + ". Largest: "
      + studentVector.lastElement().getName() + ", "
      + studentVector.lastElement().getSuBox());

    // sort studentVector using insertion sort and the vowel comparator
    studentVector.insertionSortComparator(vowelComp);
    // print out the answer to the third question
    System.out.println("3. " + studentVector.lastElement().getName());

    /* For each Student in studentVector, create an Association for the address,
    * unless that address is UNKNOWN.
    */
    for (int i = 0; i < studentVector.size(); i++) {
      String address = studentVector.get(i).getAddress();
      assocHelper(addressVector, address);
    }

    // sort addressVector using insertion sort and the address comparator
    addressVector.insertionSortComparator(addressComp);
    // create an empty array to hold Students at most-lived-at address
    MyVector<String> addressStudents = new MyVector<String>();
    // create variable for most-lived-at address
    String addressMost = addressVector.lastElement().getKey();
    /** For each Student in studentVector, check if they share the same address
    * as the most-lived-at address. If they do, add them to addressArray
    */
    for (int j = 0; j < studentVector.size(); j++) {
      if (studentVector.get(j).getAddress().equals(addressMost)) {
        addressStudents.add(studentVector.get(j).getName());
      }
    }

    // print out the answer to the fourth question
    System.out.print("4. " + "Address: "
      + addressVector.lastElement().getKey() + " Names: ");
    for (int k = 0; k < addressStudents.size(); k++) {
      System.out.print(addressStudents.get(k) + ", ");
    }

    /* For each Student in studentVector, create an Association for the area
    * code, unless Student's phone number doesn't exist as indicated by a -1.
    */
    for (int l = 0; l < studentVector.size(); l++) {
      String str = String.valueOf(studentVector.get(l).getHomePhone());
      if (str.length() >= 3) {
        String areaCode = str.substring(0, 3);
        assocHelper(areaCodeVector, areaCode);
      }
    }

    // sort areaCodeVector using insertion sort and the area code comparator
    areaCodeVector.insertionSortComparator(areaCodeComp);
    // print out extra line of space
    System.out.println();
    // print out the answer to the fifth question
    System.out.print("5. " + "Area codes: ");
    for (int m = 0; m < areaCodeVector.size(); m++) {
      if (m > 10) {
        break;
      } else {
        System.out.print(areaCodeVector.get(areaCodeVector.size() - (1 + m)).getKey() + ", ");
      }
    }
  }
}

// I am the sole author of this repository.

import java.util.Comparator;
import structure5.*;

/** StudentAddressComparator is a Student Comparator for Students' names.
*/
class StudentNameComparator implements Comparator<Student> {
  /**
	* Compares two Students' names by comparing the characters of their names.
  * @param a is a Student object.
  * @param b is a Student object.
	* @post returns the Student's name that comes first in the alphabet.
	* @return the Student's name that comes first in the alphabet.
	*/
  public int compare(Student a, Student b) {
    return a.getName().compareTo(b.getName());
  }
}

/** StudentAddressComparator is a Student Comparator for Students' SU box
* numbers.
*/
class StudentSuBoxComparator implements Comparator<Student> {
  /**
	* Compares two Students' SU box numbers by returning the difference between
  * the two.
  * @param a is a Student object.
  * @param b is a Student object.
	* @post returns the difference between their two SU box numbers.
	* @return the difference between their two SU box numbers.
	*/
  public int compare(Student a, Student b) {
    return a.getSuBox() - b.getSuBox();
  }
}

/** StudentVowelComparator is a Student Comparator for the number of vowels in
* students names.
*/
class StudentVowelComparator implements Comparator<Student> {

  /**
  * Method counts the number of vowels in a given String.
  * @param name is a given String.
  * @post returns the number of vowels in the given String.
  * @return the number of vowels in the given String.
  */
  public int countVowels(String name) {
    String str = name.toLowerCase();
    int count = 0;
    for (int i = 0; i < str.length(); i++) {
      if (str.charAt(i) == 'a' || str.charAt(i) == 'e' || str.charAt(i) == 'i'
      || str.charAt(i) == 'o' || str.charAt(i) == 'u') {
        count++;
      }
    }
    return count;
  }

  /**
	* Compares two Students' names by comparing the number of vowels in them.
  * @param a is a Student object.
  * @param b is a Student object.
	* @post returns the Student's name with the most vowels in it.
	* @return the Student's name with the most vowels in it.
	*/
  public int compare(Student a, Student b) {
    return countVowels(a.getName()) - countVowels(b.getName());
  }
}

/** StudentAddressComparator is a Student Comparator for Students' addresses.
*/
class StudentAddressComparator implements Comparator<Association<String, Integer>> {
  /**
	* Compares Students' addresses by the number of Students who live there
  * @param a is an Assocation of an address and number of Students living there
  * @param b is an Assocation of an address and number of Students living there
	* @post returns the address that has more Students living there.
	* @return the address that has more Students living there.
	*/
  public int compare(Association<String, Integer> a, Association<String, Integer> b) {
    return a.getValue().compareTo(b.getValue());
  }
}

/** StudentAddressComparator is a Student Comparator for Students' home phone
* numbers by their area code.
*/
class StudentAreaCodeComparator implements Comparator<Association<String, Integer>> {
  /**
	* Compares Students' home phone number area codes.
  * @param a is Assocation of area codes and numbers of Students who have them.
  * @param b is Assocation of area codes and numbers of Students who have them.
	* @post returns the area code that has more Students who have it.
	* @return the area code that has more Students who have it.
	*/
  public int compare(Association<String, Integer> a, Association<String, Integer> b) {
    return a.getValue().compareTo(b.getValue());
  }
}

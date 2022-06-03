// I am the sole author of this repository.

import structure5.*;
import java.util.Comparator;

/**
* MyVector extends the structure5 Vector class and implements the Comparator
* interface, as well as a sort method, which can be used to sort class objects.
*/
public class MyVector<E> extends Vector<E> {

  /**
  * MyVector default constructor calls the structure5 parent class, initializing
  * the protected fields of the parent class.
  */
  public MyVector() {
    super();
  }

  /**
	* Sorts a vector using the insertion sort method and a Comparator.
  * @param c is a Comparator that compares objects of a certain class.
	* @post sorts the vector it is called on using the insert sort method and by
  * comparing objects in the vector using the given Comparator c as a parameter.
	*/
  public void insertionSortComparator(Comparator<E> c) {
    int numSorted = 1; // number of values in place
		while (numSorted < size()) {
			E temp = get(numSorted); // first unsorted value
			int index = numSorted;
			//while(index > 0 && temp < MyVector[index - 1]) {
			while(index > 0 && c.compare(temp, get(index - 1)) < 0) {
				set(index, get(index - 1));
				index--;
			}
			//MyVector[index] = temp; // reinsert value
			set(index, temp);
			numSorted++;
    }
  }
}

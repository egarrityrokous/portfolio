// We are the sole authors of this repository.

import structure5.*;

/**
* The Student class is a representation of a Williams College student, including
* their name and the classes they are taking.
*/
public class Student {
	protected String name;
  protected Vector<String> classes;

  /**
	* Default constructor creates an empty Student
	* @pre none
	* @post instantiates all of the Student class's instance variables to empty
	* versions of their respective object types
	*/
  public Student() {
    name = "";
    classes = new Vector<String>();
  }

	/**
	* Gets a Student's name.
	* @post returns a Student's name.
	* @return a Student's name.
	*/
	public String getName() {
    return name;
  }

  /**
	* Gets a Student's classes
	* @post returns a Student's classes.
	* @return a Student's classes.
	*/
	public Vector<String> getClasses() {
    return classes;
  }

	/**
	* Gives a Student a new vector of classes
	* @param newClasses is vector of Strings representing a Student's new classes
	* @pre newClasses is not null
	* @post sets classes to newClasses
	*/
  public void setClasses(Vector<String> newClasses) {
		Assert.pre(!newClasses.equals(null), "Student's new classes should not be null.");
    classes = newClasses;
  }

	/**
	* Gives a Student a name
	* @param theName is a String representing the name you are giving a Student
	* @pre theName is not null
	* @post sets name to theName
	*/
  public void setName(String theName) {
		Assert.pre(!theName.equals(null), "Student's name should not be null.");
    name = theName;
  }

	/**
	* toString method prints a String representation of the Student class.
	* @post returns a String representation of the Student class.
	* @return a String representation of the Student class.
	*/
  public String toString() {
    return getName() + ": " + "\n" + getClasses().get(0) + "\n" + getClasses().get(1)
			+ "\n" + getClasses().get(2) + "\n" + getClasses().get(3) + "\n";
	}

	public static void main(String[] args) {

	}
}

// I am the sole author of this repository.

import structure5.*;

/**
* The Student class is a representation of a Williams College student, including
* their name, address, campus phone number, SU box number, and home phone number
*/
public class Student {
	protected String name;
  protected String address;
  protected long campusPhone;
	protected int suBox;
	protected long homePhone;

	/**
	* A constructor for Student class which instantiates all of the class's
	* instance variables.
	* @param theName is a Student's name
	* @param theAddress is a Student's address
	* @param theCampusPhone is a Student's campus phone number
	* @param theSuBox is a Student's SU box number
	* @param theHomePhone is a Student's home phone number
	* @pre theName should not be an empty string
	* @post instantiates all of the Student class's instance variables
	*/
	public Student(String theName, String theAddress, long theCampusPhone, int theSuBox, long theHomePhone) {
		Assert.pre(theName != "", "Student should have a name.");
		name = theName;
		address = theAddress;
		campusPhone = theCampusPhone;
		suBox = theSuBox;
		homePhone = theHomePhone;
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
	* Gets a Student's address.
	* @post returns a Student's address.
	* @return a Student's address.
	*/
	public String getAddress() {
    return address;
  }

	/**
	* Gets a Student's campus phone number.
	* @post returns a Student's campus phone number
	* @return a Student's campus phone number.
	*/
	public long getCampusPhone() {
    return campusPhone;
  }

	/**
	* Gets a Student's SU box number.
	* @post returns a Student's SU box number
	* @return a Student's SU box number.
	*/
	public int getSuBox() {
    return suBox;
  }

	/**
	* Gets a Student's home phone number.
	* @post returns a Student's home phone number
	* @return a Student's home phone number.
	*/
	public long getHomePhone() {
    return homePhone;
  }

	/**
	* Gives a Student a new campus phone number
	* @param newCampus Phone is an int representing a Student's new campus phone number.
	* @pre newCampusPhone is an int greater than 0
	* @post sets campusPhone to newCampusPhone
	*/
  public void setCampusPhone(int newCampusPhone) {
		Assert.pre(newCampusPhone > 0, "campus phone number should be greater than 0.");
    campusPhone = newCampusPhone;
  }

	/**
	* Gives a Student a new SU box number
	* @param newSuBox is an int representing a Student's new SU box number.
	* @pre newSuBox is an int greater than 0
	* @post sets suBox to newSuBox
	*/
	public void setSuBox(int newSuBox) {
		Assert.pre(newSuBox > 0, "SU box number should be greater than 0.");
		suBox = newSuBox;
	}

	/**
	* Gives a Student a new home phone number.
	* @param newHomePhone is an int representing a Student's new home phone number.
	* @pre newHomePhone is an int greater than 0
	* @post sets homePhone to newHomePhone.
	*/
	public void setHomePhone(int newHomePhone) {
		Assert.pre(newHomePhone > 0, "home phone number should be greater than 0.");
    homePhone = newHomePhone;
  }

	/**
	* toString method prints a String representation of the Student class.
	* @post returns a String representation of the Student class.
	* @return a String representation of the Student class.
	*/
  public String toString() {
    return getName() + ", " + getAddress() + ", " + getCampusPhone() + ", "
			+ getSuBox() + ", " + getHomePhone() + ".";
	}
}

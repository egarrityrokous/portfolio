// We are the sole authors of this repository.

import structure5.*;
import java.util.Scanner;
import java.util.Iterator;

/**
* A GraphListUndirected implementation solving the final exam scheduling problem
* and extension 1 of lab10
*/
public class ExamScheduler {

  // instance variable for a Vector of Student objects
  protected Vector<Student> students;

  // instance variable graph for the GraphListUndirected implementation
  protected GraphListUndirected<String, Integer> graph;

  // instance variable for a Vector of Vectors of courses which are Strings
  protected Vector<Vector<String>> slots;

  /**
  * A default constructor that constructs an empty ExamScheduler
  * @pre none
  * @post instantiates all the ExamScheduler's instance variables as empty
  * versions of their object types
  */
  public ExamScheduler() {
    graph = new GraphListUndirected<String, Integer>();
    students = readInFile();
    slots = new Vector<Vector<String>>();
  }

  /**
  * Reads in a file and creates a Vector of Student objects based on the lines
  * given by the file
  * @pre none
  * @post returns a Vector of Student objects
  * @return a Vector of Student objects
  */
  public Vector<Student> readInFile() {
    // create an acculumator Vector of Students
    Vector<Student> students = new Vector<Student>();
    Scanner sc = new Scanner(System.in);
    while (sc.hasNextLine()) {
      // name gets first given line; classes get four next given lines
      String name = sc.nextLine();
      String class1 = sc.nextLine();
      String class2 = sc.nextLine();
      String class3 = sc.nextLine();
      String class4 = sc.nextLine();
      // create an accumulator Vector of Strings and add the classes to it
      Vector<String> classes = new Vector<String>();
      classes.add(class1);
      classes.add(class2);
      classes.add(class3);
      classes.add(class4);
      // create a local variable for a given student
      Student s1 = new Student();
      // identify and set the correct name for the given student
      s1.setName(name);
      // identify and set the correct Vector of courses for the given student
      s1.setClasses(classes);
      // build graph with each student's classes and the correct edges  b/w them
      addStudentClasses(s1.getClasses());
      // add local student to our Vector of Student objects
      students.add(s1);
    }
    // return our accumulated Vector of Students
    return students;
  }

  /**
  * Builds the graph with classes as vertices and correct edges between vertices
  * @pre classes is not null
  * @post builds graph with each distinct class as a vertice and the correct
  * edges between them
  */
  public void addStudentClasses(Vector<String> classes) {
    Assert.pre(!classes.equals(null), "classes should not be null.");
    // adds classes as vertices if they do not exist
    for (int i = 0; i < classes.size(); i++) {
      if (!graph.contains(classes.get(i))) {
        graph.add(classes.get(i));
      }
    }
    // adds edges between classes if they do not exist, else increasing weight of edge by 1
    for (int i = 0; i < classes.size() - 1; i++) {
      for (int j = i + 1; j < classes.size(); j++) {
        if (!graph.containsEdge(classes.get(i), classes.get(j))) {
          graph.addEdge(classes.get(i), classes.get(j), 1);
        } else {
          int currentEdge = graph.getEdge(classes.get(i), classes.get(j)).label();
          graph.getEdge(classes.get(i), classes.get(j)).setLabel(++currentEdge);
        }
      }
    }
  }

  /**
  * Builds a final exam schedule, which is a Vector of Vectors of Strings that
  * are the courses for the final exams
  * @pre none
  * @post returns a Vector of Vectors of Strings that represent the slots for
  * for each final exam
  * @return a Vector of Vectors of Strings
  */
  public Vector<Vector<String>> makeFinalExamSchedule() {
      while (!isEmptyGraph()) {
      Iterator<String> it = graph.iterator();
        while (it.hasNext()) {
          Vector<String> slot = new Vector<String>();
          String curClass = it.next();
          // if curClass has not been visited yet, add it to a final exam slot
          if (!graph.isVisited(curClass)) {
            slot.add(curClass);
          }
            // create a second iterator for the next class
            Iterator<String> two = graph.iterator();
              while (two.hasNext()) {
                String nextClass = two.next();
                // check if nextClass has been visited yet
                if (!graph.isVisited(nextClass)) {
                  /* check if nextClass is equal to curClass and if there is an
                  edge between nextClass and another class in an exam slot */
                  if (nextClass != curClass && !containsEdgeInSlots(slot, nextClass)) {
                    // add nextClass to slot and visit nextClass
                    slot.add(nextClass);
                    graph.visit(nextClass);
                  }
                }
              }
              // visit curClass and add current final exam slot to slots
              graph.visit(curClass);
              slots.add(slot);
        }
      }
      // return slots that represent the final exam schedule
      return slots;
  }

  /**
  * Helper method for makeFinalExamSchedule checks if there is an edge between
  * nextClass and any other class in the current slot were checking
  * @pre slot is not null
  * @pre nextClass is not null
  * @post return true if there is an edge between nextClass and any class in
  * slot; false otherwise
  * @return true if there is an edge between nextClass and any class in slot;
  * false otherwise
  */
  public boolean containsEdgeInSlots(Vector<String> slot, String nextClass) {
    Assert.pre(!slot.equals(null), "final exam slot should not be null.");
    Assert.pre(!nextClass.equals(null), "next class should not be null.");
    // check if there is an edge between nextClass and any class in slot
    for (int i = 0; i < slot.size(); i++) {
      if (graph.containsEdge(slot.get(i), nextClass)) {
        return true;
      }
    }
    return false;
  }

  /**
  * makeFinalExamSchedule helper method checks if graph has a non-visited node
  * @pre none
  * @post return true if graph has node that's not been visited; false otherwise
  * @return true if graph has node that's not been visited; false otherwise
  */
  public boolean isEmptyGraph() {
    Iterator<String> it = graph.iterator();
    while (it.hasNext()) {
      // if there is a node in graph has not been visited yet, return false
      if (!(graph.isVisited(it.next()))) {
        return false;
      }
    }
    // else, return true
    return true;
  }

  /**
  * Prints out basic final exam schedule
  * @pre slots is not null
  * @post prints out the slots for a final exam schedule, one slot for each
  * final exam period
  */
  public void printFinalExamSchedule(Vector<Vector<String>> slots) {
    Assert.pre(!slots.equals(null), "final exam slots should not be null.");
    // find each slot in slots
    for (int i = 0; i < slots.size(); i++) {
      // only account for non-empty slots in slots
      if (!slots.get(i).isEmpty()) {
        Vector<String> curSlot = slots.get(i);
        String stringToPrint = "Slot " + (i + 1) + ": ";
        // add correct class to each slot in slots
        for (int j = 0; j < curSlot.size(); j++) {
          stringToPrint += curSlot.get(j) + " ";
        }
        // print out each slot in slots, line by line
        System.out.println(stringToPrint);
      }
    }
  }

  /**
  * For lab10 extension 1 (for main credit), print out the exams in alphabetical
  * order, along with each student taking the exams
  * @pre slots is not null
  * @pre students is not null
  * @post prints out the slots for a final exam schedule in order, one slot for
  * each final exam period, along with each student taking the exam
  */
  public void printOrderedExams(Vector<Vector<String>> slots, Vector<Student> students) {
    Assert.pre(!slots.equals(null), "final exam slots should not be null.");
    Assert.pre(!students.equals(null), "Vector of students should not be null.");
    /* use helper method to create an OrderedVector for the exam slots and the
    students taking them */
    OrderedVector<ComparableAssociation<String, Vector<Student>>> sortedCourses = sortCourses(slots, students);
    // create an iterator for the sorted courses
    Iterator<ComparableAssociation<String, Vector<Student>>> iter = sortedCourses.iterator();
    while (iter.hasNext()) {
      // iterate over associations of courses and their respective students
      ComparableAssociation<String, Vector<Student>> course = iter.next();
      // use helper method to add correct student names to each print statement
      String stringToPrint = course.getKey()
        + " -- students taking this course: " + studentNames(course.getValue());
      System.out.println(stringToPrint);
    }
  }

  /**
  * Helper method for printOrderedExams creates a String of students taking each
  * course's final exam
  * @pre students is not null
  * @post return a String of students taking each course's final exam
  * @return a String of students taking each course's final exam
  */
  public String studentNames(Vector<Student> students) {
    Assert.pre(!students.equals(null), "Vector of students should not be null.");
    String names = "";
    // for each student in students, add only their names to accumulator string
    for (int i = 0; i < students.size(); i++) {
      names += students.get(i).getName() + ". ";
    }
    return names;
  }

  /**
  * Helper method for sortCourses that creates a Vector of Student objects
  * that are in a given course
  * @pre students is not null
  * @pre c is not null
  * @post return a Vector of Strings that are students in a given course
  * @return a Vector of Strings that are students in a given course
  */
  public Vector<Student> courseStudents(Vector<Student> students, String c) {
    Assert.pre(!students.equals(null), "Vector of students should not be null.");
    Assert.pre(!c.equals(null), "course name should not be null.");
    Vector<Student> courseStuds = new Vector<Student>();
    // for each student in students, get the clases they are in
    for (int i = 0; i < students.size(); i++) {
      Vector<String> classes = students.get(i).getClasses();
      // check if any of the classes a student is in matches the given class c
      for (int j = 0; j < classes.size(); j++) {
        // if it does, add the student to courseStuds
        if (classes.get(j).equals(c)) {
          courseStuds.add(students.get(i));
        }
      }
    }
    return courseStuds;
  }

  /**
  * Helper method for printOrderedExams that creates an OrderedVector of
  * Comparable Associations with courses as keys and Vectors of Students who
  * take that course as values
  * @pre slots is not null
  * @pre students is not null
  * @post return a Vector of Strings that are students in a given course
  * @return a Vector of Strings that are students in a given course
  */
  public OrderedVector<ComparableAssociation<String, Vector<Student>>> sortCourses(Vector<Vector<String>> slots, Vector<Student> students) {
    Assert.pre(!slots.equals(null), "final exam slots should not be null.");
    Assert.pre(!students.equals(null), "Vector of students should not be null.");
    // create our accumulator OrderedVector
    OrderedVector<ComparableAssociation<String, Vector<Student>>> sortedCourses
      = new OrderedVector<ComparableAssociation<String, Vector<Student>>>();
    // for each slot in slots, create a Vector of Students for that given course
    for (int i = 0; i < slots.size(); i++) {
      for (int j = 0; j < slots.get(i).size(); j++) {
        // use helper method to create local Vector of Students for each course
        Vector<Student> courseStuds = courseStudents(students, slots.get(i).get(j));
        // create local ComparableAssociation with each course as key and local Vector of Students as value
        ComparableAssociation<String, Vector<Student>> course
          = new ComparableAssociation<String, Vector<Student>>(slots.get(i).get(j), courseStuds);
        // add local ComparableAssocation course to our accumulator variable sortedCourses
        sortedCourses.add(course);
      }
    }
    // return our accumulator variable
    return sortedCourses;
  }

  /**
  * For lab10 extension 2 (for extra credit), print out the students in
  * alphabetical order with their individual exam schedule
  * @pre slots is not null
  * @pre students is not null
  * @post prints out the students in alphabetical order with their individual
  * exam schedule
  */
  public void printStudentSchedules(Vector<Vector<String>> slots, Vector<Student> vecStudents) {
    Assert.pre(!slots.equals(null), "final exam slots should not be null.");
    Assert.pre(!students.equals(null), "Vector of students should not be null.");
    // accumulator index variable
    int index = 0;
    /* while Vector of Students is not empty, find the name with the highest
    alphabetical priority and updates index variable */
    while (!vecStudents.isEmpty()) {
      for (int i = 0; i < vecStudents.size(); i++) {
        String priority = vecStudents.get(0).getName();
        if (priority.compareTo(vecStudents.get(i).getName()) >= 0) {
          priority = vecStudents.get(i).getName();
          index = i;
        }
      }
      // prints the name of the student with the highest alphabetical priority
      System.out.println(vecStudents.get(index).getName());
      // temporary variable of the given exams offered in each slot
      Vector<Vector<String>> tempSlots = slots;
      /* checks each exam slot to see which exam student will take in given slot
      and then prints each name of the exam that student is taking */
      for (int i = 0; i < tempSlots.size(); i++) {
        if (tempSlots.get(i).contains(vecStudents.get(index).getClasses().get(0))) {
          System.out.println("Slot " + (i + 1) + ": " + vecStudents.get(index).getClasses().get(0));
        }
        if (tempSlots.get(i).contains(vecStudents.get(index).getClasses().get(1))) {
          System.out.println("Slot " + (i + 1) + ": " + vecStudents.get(index).getClasses().get(1));
        }
        if (tempSlots.get(i).contains(vecStudents.get(index).getClasses().get(2))) {
          System.out.println("Slot " + (i + 1) + ": " + vecStudents.get(index).getClasses().get(2));
        }
        if(tempSlots.get(i).contains(vecStudents.get(index).getClasses().get(3))) {
          System.out.println("Slot " + (i + 1) + ": " + vecStudents.get(index).getClasses().get(3));
        }
      }
      /* removes student from our temporay vec of students, given as a parameter
      after each student object and their respective exams have been printed */
      vecStudents.remove(index);
    }
  }

  /**
  * Main method for testing
  */
  public static void main(String[] args) {
    // creates ExamScheduler object and graph of time slots to take given exams
    ExamScheduler exams = new ExamScheduler();
    // stores our final exam schedule
    Vector<Vector<String>> schedule = exams.makeFinalExamSchedule();
    // prints our final exam schedule
    exams.printFinalExamSchedule(schedule);
    // stores our Vector of Students
    Vector<Student> students = exams.students;
    /* prints the exams in alphabetical order and students taking each exam for
    extension 1 (for main credit) */
    exams.printOrderedExams(schedule, students);
    /* create a temporary vec of students to give as a parameter when calling
    printStudentSchedules method for extension 2 (for extra credit) */
    Vector<Student> tempStudents = new Vector<Student>();
    for (int i = 0; i < students.size(); i++) {
      tempStudents.add(students.get(i));
    }
    /* prints students in alphabetical order and exam schedules for extension 2
    (for extra credit) */
    exams.printStudentSchedules(schedule, tempStudents);
  }
}

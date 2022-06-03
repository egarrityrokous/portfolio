# CS136 Lab: Spot the Difference

## Useful Links
* [Course Homepage](https://williams-cs.github.io/cs136s22-www/) (with TA schedule)
* [Lab Webpage](https://williams-cs.github.io/cs136s22-www/assets/labs/diff/diff.html)
* [structure5](http://www.cs.williams.edu/~bailey/JavaStructures/doc/structure5/index.html) documentation
* [GitHub markdown](https://guides.github.com/features/mastering-markdown/) syntax


## Repository Contents
This repository contains the starter files for writing and testing your diff implementation.

## Sample Files

The following are the sample files included with the starter code.  They are listed in increasing order of complexity---as you add more to your code, you will be able to handle more sample files.

### After Implementing the Base Case

After implementing the base case (but without any recursive calls), running
```
$ java Diff samples/verySmallA.txt samples/empty.txt
```
should give output exactly matching the contents of `samples/emptySolution.txt`.

### After Task 1

After task 1, `diffHelper` should be fully implemented in `Diff.java`.  Then running 
```
$ java Diff samples/verySmallA.txt samples/verySmallB.txt
```
should give output exactly matching the contents of `samples/verySmallSolution.txt`.

Furthermore, running 
```
$ java Diff samples/smallA.txt samples/smallB.txt
```
should give output exactly matching the contents of `samples/smallSolution.txt`.

### After Task 2
After task 2, `diffHelper` should be fully implemented in `HashDiff.java`, including hash table calls to speed up execution.  The `hashCode()` method of `IntPair.java` should be implemented as well.  Then running 
```
$ java HashDiff samples/maSenate2016.txt samples/maSenate2020.txt
```
should give output exactly matching the contents of `samples/maSenateSol.txt`.

### After Task 3
After task 3, `diffHelper` should be fully implemented in `BetterHashDiff.java`, including hash table calls to speed up execution.  The `hashCode()` method of `BetterIntPair` should be implemented as well, and the hash table in `BetterHashDiff.java` should use `BetterIntPair`.  Then running 
```
$ java BetterHashDiff samples/whosonfirst.txt samples/whosonfirst2.txt
```
should give output exactly matching the contents of `samples/whosonfirstSol.txt`.

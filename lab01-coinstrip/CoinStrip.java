/* I am the sole author of the work in this repository. Clay Mizgerd '22 helped
* me interpret syntactical errors.
*/
import java.util.Random;
import java.util.Scanner;

/* The class CoinStrip creates the CoinStrip game board, which is stored as an
 * array, prints the current state of the board, prompts players to input moves,
 * checks if those moves are valid, makes those moves on the game board if
 * they are valid, prints a string representation of the game board as well as
 * which player won the game, and prints how many coins and what positions
 * they're at, at any given time.
 */
public class CoinStrip {
    final Random rand = new Random();
    protected int[] coins;

    // randomizes the number of coins between 3 and 8 coins
    public final int numCoins = rand.nextInt(6) + 3;

    /** Sets up the CoinStrip game board initially and populates it with a
    * random number of coins.
    */
    public CoinStrip() {
        // creates a game board, coins, with random length of 10-20 spaces
        int gameBoard = rand.nextInt(11) + 10;
        coins = new int[gameBoard];

        // keeps track of the number of coins currently on the game board
        int coinsOnBoard = 0;

        // randomly assigns coins onto the game board, coins
        while (coinsOnBoard < numCoins) {
            int coinIndex = rand.nextInt(coins.length);
            if (coins[coinIndex] == 0) {
              coins[coinIndex] = coinsOnBoard + 1;
              coinsOnBoard++;
            }
        }
    }

    /** Checks to see if a move is valid: that the requested move doesn't
    * jump over other coins, and the requested index exists on the game board.
    * @param whichCoin: the number of the coin a player would like to move.
    * @param numSpaces: number of spaces to move the coin (left).
    * @return true if the move is valid, false if invalid.
    */
    public boolean isValidMove(int whichCoin, int numSpaces) {
        // Checks if numSpaces is less than 1, an invalid move
        if (numSpaces < 1) {
            return false;
        }

        // Checks if requested move jumps over another coin
        for (int coinIndex = 0; coinIndex < coins.length; coinIndex++) {
            if (coins[coinIndex] == whichCoin) {
                if (coinIndex - numSpaces < 0) {
                    return false;
                }
                // Checks if a coin is already in the requested space
                for (int i = coinIndex - numSpaces; i < coinIndex; i++) {
                    if (coins[i] != 0) {
                        return false;
                    }
                }
                return true;
            }
        }
        return false;
    }

    /** Updates the game board to reflect a valid move.
     * Behavior is undefined if the described move is invalid.
     */
    public void makeMove(int whichCoin, int numSpaces) {
        for (int coinIndex = 0; coinIndex < coins.length; coinIndex++) {
            if (coins[coinIndex] == whichCoin) {
                // sets new coin position to whichCoin and resets old one to 0
                coins[coinIndex - numSpaces] = whichCoin;
                coins[coinIndex] = 0;
            }
        }
    }

    /** Returns true if the game is over, when all the coins are at the leftmost
    * positions on the CoinStrip game board, without spaces.
    * @return true if the game is over, false otherwise.
    */
    public boolean isGameOver() {
        for (int coinIndex = 0; coinIndex < numCoins; coinIndex++) {
            if (coins[coinIndex] == 0) {
                return false;
            }
        }
        return true;
    }

    /** Returns the number of coins on the CoinStrip gameboard.
     * @return the number of coins on the CoinStrip gameboard.
     */
    public int getNumCoins() {
        return numCoins;
    }

    /** Returns the 0-indexed location of a specific coin. Coins are
     * also zero-indexed. So, if the CoinStrip had 3 coins, the coins
     * would be indexed 0, 1, or 2.
     * @param coinNum the 0-indexed coin number
     * @return the 0-indexed location of the coin on the CoinStrip
     */
    public int getCoinPosition(int coinNum) {
        // keeps track of the current number of coin count
        int coinCount = 0;

        // keeps track of the current coin index
        int coinIndex = 0;

        // iterates over the game board, coins, until coinCount equals coinNum
        while (coinCount != coinNum) {
            if (coins[coinIndex] != 0) {
                coinCount++;
            }
            coinIndex++;
        }
        return coinIndex - 1;
    }

    /* prints a string representation of the board, on which spaces are dollar
    * signs and coins are integers.
    */
    public final String toString() {
        String board = " ";
        for (int coinIndex = 0; coinIndex < coins.length; coinIndex++) {
            if (coins[coinIndex] == 0) {
		            board += "$ ";
	          } else {
		            board += coins[coinIndex] + " ";
            }
        }
        return board;
    }

    /**
     * `public static void main(String[] args)` is a program's entry point.
     * This main method implements the functionality to play the Coinstrip game.
     * @param Command-line arguments are ignored.
     */
    public static void main(String[] args) {
        System.out.println("Welcome to the Silver Dollar Game!");
        CoinStrip coins = new CoinStrip();
        System.out.println(coins);

        Scanner in = new Scanner(System.in);

      	// keeps track of which player is requesting the moves
      	int player = 1;

      	// this loop continues until isGameOver returns true
      	while (!coins.isGameOver()) {
      	    // prompts user for whichCoin and numSpaces
      	    int whichCoin;
            int numSpaces;

            /* while the isGameOver returns false, players are prompted for
            * their moves
            */
            while (true) {
            		System.out.print("Player " + player
                    + ", enter a coin number you wish to move: ");
            		whichCoin = in.nextInt();

            		System.out.print("Player " + player
                    + ", enter a number of spaces you wish to move the coin: ");
            		numSpaces = in.nextInt();

            		// if requested move is valid, break loop and move the coin
            		if (coins.isValidMove(whichCoin, numSpaces)) {
            		    break;
            		} else {
            		    System.out.println("invalid move");
            		}
      	    }

            // makes requested move and prints new, current game board state
      	    coins.makeMove(whichCoin, numSpaces);
      	    System.out.println(coins);

            /* If isGameOver returns true, player who won the game is displayed.
            * Else, players switch turns.
            */
            if (coins.isGameOver()) {
            		System.out.print("Player " + player + " wins!");
            } else {
            		if (player == 1) {
            		    player = 2;
            		} else {
            		    player = 1;
            		}
      	    }
      	}
    }
}
